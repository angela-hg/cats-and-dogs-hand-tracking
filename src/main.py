import pygame
import random
import cv2
import mediapipe as mp
import sys
import os

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CAT_SIZE = 100
DOG_SIZE = 100
COIN_RADIUS = 12
DOG_COUNT = 4
DOG_SPEED = 1

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
CAT_IMG_PATH = os.path.join(ASSETS_DIR, "cat.png")
DOG_IMG_PATH = os.path.join(ASSETS_DIR, "dog.png")
MUSIC_PATH = os.path.join(ASSETS_DIR, "cat_song.wav")

def init_hand_tracker():
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam not found. Exiting.")
        sys.exit(1)
    return mp_hands, mp_draw, hands, cap

def get_hand_position(cap, hands, mp_hands, mp_draw):
    ok, frame = cap.read()
    if not ok:
        return None

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            index_tip = hand_lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_tip.x * SCREEN_WIDTH)
            y = int(index_tip.y * SCREEN_HEIGHT)
            mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)
            break
    else:
        x, y = None, None

    small = cv2.resize(frame, (320, 240))
    cv2.imshow("Hand Tracking", small)
    cv2.waitKey(1)

    if x is None or y is None:
        return None
    return x, y

def spawn_coin():
    x = random.randint(0, SCREEN_WIDTH - COIN_RADIUS * 2)
    y = random.randint(0, SCREEN_HEIGHT - COIN_RADIUS * 2)
    return pygame.Rect(x, y, COIN_RADIUS * 2, COIN_RADIUS * 2)

def spawn_dog():
    x = random.randint(0, SCREEN_WIDTH - DOG_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - DOG_SIZE)
    return pygame.Rect(x, y, DOG_SIZE, DOG_SIZE)

def clamp_player(rect):
    rect.x = max(0, min(rect.x, SCREEN_WIDTH - rect.width))
    rect.y = max(0, min(rect.y, SCREEN_HEIGHT - rect.height))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cats and Dogs")
    clock = pygame.time.Clock()

    # Load assets
    try:
        cat_img = pygame.transform.scale(pygame.image.load(CAT_IMG_PATH), (CAT_SIZE, CAT_SIZE))
        dog_img = pygame.transform.scale(pygame.image.load(DOG_IMG_PATH), (DOG_SIZE, DOG_SIZE))
    except Exception as e:
        print("Error loading images:", e)
        sys.exit(1)

    # Music
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Warning: could not load music:", e)

    # Hand tracker
    mp_hands, mp_draw, hands, cap = init_hand_tracker()

    player = pygame.Rect(300, 250, CAT_SIZE, CAT_SIZE)
    coins = [spawn_coin()]
    dogs = [spawn_dog() for _ in range(DOG_COUNT)]
    score = 0
    font = pygame.font.SysFont("Arial", 30)
    running = True

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Hand control
            pos = get_hand_position(cap, hands, mp_hands, mp_draw)
            if pos:
                player.x, player.y = pos
                clamp_player(player)

            # Update dogs
            for d in dogs:
                d.x += random.choice([-DOG_SPEED, DOG_SPEED])
                d.y += random.choice([-DOG_SPEED, DOG_SPEED])
                d.x = max(0, min(d.x, SCREEN_WIDTH - DOG_SIZE))
                d.y = max(0, min(d.y, SCREEN_HEIGHT - DOG_SIZE))

            # Collisions with coins
            for c in coins[:]:
                if player.colliderect(c):
                    coins.remove(c)
                    score += 1
                    coins.append(spawn_coin())

            # Collisions with dogs
            for d in dogs:
                if player.colliderect(d):
                    running = False

            # Draw
            screen.fill((0, 0, 0))
            screen.blit(cat_img, (player.x, player.y))
            for c in coins:
                pygame.draw.circle(screen, (255, 255, 0), c.center, COIN_RADIUS)
            for d in dogs:
                screen.blit(dog_img, d.topleft)

            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)
    finally:
        # Cleanup
        try:
            cap.release()
        except Exception:
            pass
        cv2.destroyAllWindows()
        pygame.quit()

if __name__ == "__main__":
    main()
