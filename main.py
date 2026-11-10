import random
import pygame
import time
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
print("Current directory:", os.getcwd())
print("Files:", os.listdir())
class TextBox:
    def __init__(self, x, y, width, height, placeholder="Type here...", max_length=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.max_length = max_length
        self.active = False
        self.font = pygame.font.Font(None, 32)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return self.text
            elif event.unicode.isprintable() and len(self.text) < self.max_length:
                self.text += event.unicode
        return None
    def draw(self, screen):
        colour = (0, 200, 255) if self.active else (150, 150, 150)
        pygame.draw.rect(screen, colour, self.rect, 2)
        display_text = self.text or self.placeholder
        text_colour = (255, 255, 255) if self.text else (130, 130, 130)
        surface = self.font.render(display_text, True, text_colour)
        screen.blit(surface, (self.rect.x + 8, self.rect.y + 8))
    def get(self):
        return self.text
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1000, 600))
icon = pygame.image.load(f"{script_dir}\logo.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Haunted House")
running = True
heart = pygame.image.load(f"{script_dir}\heart.png")
heart = pygame.transform.scale(heart, (30, 30))
golden_heart = pygame.image.load(f"{script_dir}\golden_heart.png")
golden_heart = pygame.transform.scale(golden_heart, (30, 30))
button1 = pygame.Rect(40, 520, 280, 60)
button2 = pygame.Rect(360, 520, 280, 60)
button3 = pygame.Rect(680, 520, 280, 60)
def riddle(question, correct_answer, wrong_answer, image_filename):
    global lives
    global running
    global currentChoiceRunning
    global button1
    global button2
    global button3
    global output
    global title
    global screen
    if lives <= 0:
        return False
    currentChoiceRunning = True
    output = pygame.font.SysFont("Arial", 30).render("Pick Answer", True, (255, 255, 255))
    answers = [(correct_answer, True), (wrong_answer, False)]
    random.shuffle(answers)
    image = pygame.image.load(f"{script_dir}\{image_filename}")
    image = pygame.transform.scale(image, (800, 300))
    while currentChoiceRunning:
        title = pygame.font.SysFont("Arial", 30).render(question, True, (255, 255, 255))
        button1_color = (85, 32, 48)
        button2_color = (85, 32, 48)
        button3_color = (85, 32, 48)
        answer1_text = pygame.font.SysFont("Arial", 30).render(answers[0][0], True, (255, 255, 255))
        answer2_text = pygame.font.SysFont("Arial", 30).render(answers[1][0], True, (255, 255, 255))
        button3_text = pygame.font.SysFont("Arial", 30).render("Eat Sweets", True, (255, 255, 255))
        screen.fill((22, 16, 32))
        for i in range(min(lives, 5)):
            screen.blit(heart, (950 - (i + 1) * 30, 10))
        for i in range(max(0, lives - 5)):
            screen.blit(golden_heart, (950 - (i + 1) * 30, 40))
        pygame.draw.rect(screen, button1_color, button1)
        pygame.draw.rect(screen, button2_color, button2)
        pygame.draw.rect(screen, button3_color, button3)
        screen.blit(answer1_text, (button1.x + 10, button1.y + 10))
        screen.blit(answer2_text, (button2.x + 10, button2.y + 10))
        screen.blit(button3_text, (button3.x + 10, button3.y + 10))
        screen.blit(title, (50, 20))
        screen.blit(image, (100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                currentChoiceRunning = False
                running = False
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                selected_answer = None
                if button1.collidepoint(mouse_pos):
                    selected_answer = answers[0][1]
                elif button2.collidepoint(mouse_pos):
                    selected_answer = answers[1][1]
                if selected_answer is not None:
                    currentChoiceRunning = False
                    is_correct = selected_answer
                    message = "Correct! You move on" if is_correct else "Wrong Answer!"
                    output = pygame.font.SysFont("Arial", 30).render(message, True, (255, 255, 255))
                    screen.blit(output, (50, 450))
                    pygame.display.flip()
                    time.sleep(1)
                    if is_correct:
                        if lives < 5:
                            lives += 1
                    else:
                        lives -= 1
                    return is_correct
                elif button3.collidepoint(mouse_pos):
                    output = pygame.font.SysFont("Arial", 30).render("You Enjoy Your Chocolate. Pick an Answer!", True, (255, 255, 255))
                    screen.blit(output, (50, 450))
                    pygame.display.flip()
                    time.sleep(0.2)
        screen.blit(output, (50, 450))
        pygame.display.flip()
    return False
riddles = [
    ("What has keys but cannot open locks?", "A piano", "A door"),
    ("What gets wetter the more it dries?", "A towel", "A sponge"),
    ("What has a face and two hands but no arms or legs?", "A clock", "A statue"),
    ("What has to be broken before you can use it?", "An egg", "A glass"),
    ("What goes up but never comes down?", "Your age", "A balloon"),
    ("What has one eye but cannot see?", "A needle", "A camera"),
    ("What can travel around the world while staying in one corner?", "A stamp", "A map"),
    ("What has many teeth but cannot bite?", "A comb", "A crocodile"),
    ("What belongs to you but other people use it more than you do?", "Your name", "Your phone"),
    ("What has a neck but no head?", "A bottle", "A giraffe"),
    ("What has four legs but cannot walk?", "A table", "A dog"),
    ("What has words but never speaks?", "A book", "A parrot"),
    ("What has a ring but no finger?", "A telephone", "A wedding ring"),
    ("What can you catch but not throw?", "A cold", "A ball"),
    ("What has a bottom at the top?", "Your legs", "A mountain"),
    ("What runs but never walks?", "A river", "A person"),
    ("What has cities but no houses, forests but no trees, and rivers but no water?", "A map", "A globe"),
    ("What can fill a room but takes up no space?", "Light", "Furniture"),
    ("What has an endless supply of letters but starts empty?", "A mailbox", "A book"),
    ("What has a head and a tail but no body?", "A coin", "A snake"),
    ("What comes down but never goes up?", "Rain", "Smoke"),
    ("What has branches but no fruit, trunk or leaves?", "A bank", "A tree"),
    ("What can you hold without ever touching it?", "Your breath", "A stone"),
    ("What has 13 hearts but no other organs?", "A deck of cards", "A hospital"),
    ("What has holes but can still hold water?", "A sponge", "A bucket"),
    ("What is always in front of you but cannot be seen?", "The future", "Your shadow"),
    ("What begins with T, ends with T and has T inside?", "A teapot", "A tent"),
    ("What has legs but doesn't move?", "A chair", "A horse"),
    ("What has a thumb and four fingers but isn't alive?", "A glove", "A hand"),
    ("What can be cracked, made, told and played?", "A joke", "A window"),
    ("What has many needles but doesn't sew?", "A pine tree", "A sewing machine"),
    ("What has an eye at the centre but is not alive?", "A hurricane", "A person"),
    ("What gets bigger the more you take away from it?", "A hole", "A pile"),
    ("What can you serve but never eat?", "A tennis ball", "A sandwich"),
    ("What has no beginning, middle or end?", "A circle", "A straight line"),
    ("What has a spine but no bones?", "A book", "A skeleton"),
    ("What has a bark but no bite?", "A tree", "A dog"),
    ("What goes through towns and over hills but never moves?", "A road", "A train"),
    ("What has ears but cannot hear?", "A cornfield", "A rabbit"),
    ("What can be opened but has no door?", "An umbrella", "A cupboard"),
    ("What has a bed but never sleeps?", "A river", "A person"),
    ("What has a tongue but cannot talk?", "A shoe", "A parrot"),
    ("What can you make that nobody can see?", "Noise", "A painting"),
    ("What is full of holes but keeps things together?", "A net", "A wall"),
    ("What has a crown but isn't a king?", "A tooth", "A prince"),
    ("What has a tail and flies but isn't a bird?", "A kite", "A plane"),
    ("What has no life but can die?", "A battery", "A flower"),
    ("What can be long or short, grown or bought, painted or left bare?", "Fingernails", "Hair"),
    ("What has four wheels and flies?", "A rubbish truck", "A helicopter"),
    ("What has a lock but no door?", "A canal", "A treasure chest"),
    ("What is easy to lift but hard to throw?", "A feather", "A rock"),
    ("What has a mouth but never eats?", "A river", "A person"),
    ("What has lots of eyes but cannot see?", "A potato", "A spider"),
    ("What has a heart that doesn't beat?", "An artichoke", "A human"),
    ("What can be lost, found, kept and broken?", "A promise", "A pencil"),
    ("What has a head but no brain?", "A cabbage", "A scientist"),
    ("What is black when clean and white when dirty?", "A blackboard", "A whiteboard"),
    ("What goes up and down but stays in the same place?", "A staircase", "An elevator"),
    ("What has five letters but becomes shorter when you add two letters?", "Short", "Long"),
    ("What can you hear but not touch or see?", "An echo", "A cloud"),
    ("What is always coming but never arrives?", "Tomorrow", "Yesterday"),
    ("What has a lot of rings but no fingers?", "A tree", "A telephone"),
    ("What can run around a garden without moving?", "A fence", "A dog"),
    ("What has pages but isn't a book?", "A calendar", "A notebook"),
    ("What has a foot but no legs?", "A ruler", "A person"),
    ("What has a face but no eyes, nose or mouth?", "A clock", "A portrait"),
    ("What is so fragile that saying its name breaks it?", "Silence", "Glass"),
    ("What has six faces and twenty-one eyes but cannot see?", "A dice", "A monster"),
    ("What can you keep after giving it to someone?", "Your word", "A present"),
    ("What is always hungry and dies if you feed it water?", "Fire", "A fish"),
    ("What has no wings but can fly?", "Time", "A bird"),
    ("What can be measured but has no length, width or height?", "Temperature", "A ruler"),
    ("What is lighter than air but a hundred people cannot lift it?", "A bubble", "A feather"),
    ("What has a golden head and a wooden body?", "A matchstick", "A hammer"),
    ("What starts with E, ends with E and contains one letter?", "An envelope", "An email"),
    ("What can go up a chimney down but cannot go down a chimney up?", "An umbrella", "Smoke"),
    ("What has two banks but no money?", "A river", "A shop"),
    ("What has a shell but isn't a turtle?", "An egg", "A crab"),
    ("What can be driven but has no wheels?", "A nail", "A car"),
    ("What has a foot on each side and one in the middle?", "A yardstick", "A tripod"),
    ("What can you see once in a minute, twice in a moment, but never in a thousand years?", "The letter M", "The letter T"),
    ("What has four eyes but cannot see?", "Mississippi", "A spider"),
    ("What kind of room has no doors or windows?", "A mushroom", "A bedroom"),
    ("What has a head, a foot and four legs?", "A bed", "A horse"),
    ("What has many stories but no characters?", "A building", "A novel"),
    ("What can travel fast without moving?", "A thought", "A bicycle"),
    ("What is always old and sometimes new, never sad but sometimes blue?", "The moon", "The sun"),
    ("What has a needle but cannot sew?", "A compass", "A sewing kit"),
    ("What can you find at the end of a rainbow?", "The letter W", "A pot of gold"),
    ("What has a mouth and a tongue but cannot speak?", "A shoe", "A person"),
    ("What is bought by the yard and worn by the foot?", "Carpet", "Shoes"),
    ("What has a thousand sheets but no paper?", "A bed", "A book"),
    ("What can be swallowed but can also swallow you?", "Pride", "Water"),
    ("What has no weight but can sink a ship?", "A hole", "An anchor"),
    ("What is always moving but never leaves its place?", "A clock's hands", "A car"),
    ("What has a face on both sides but no body?", "A coin", "A mirror"),
    ("What gets sharper the more you use it?", "Your brain", "A pencil"),
    ("What can be seen in water but never gets wet?", "A reflection", "A fish"),
    ("What has a lid but no box?", "An eye", "A suitcase"),
    ("What has a beginning but no end, and an end but no beginning?", "A circle", "A line")
]
while running:
    lives = 5
    nextChoice = ""
    currentChoiceRunning = True
    output = pygame.font.SysFont("Arial", 30).render("You can either enter the house, sneak in from the back, or run away from it.", True, (255, 255, 255))
    while currentChoiceRunning:
        title = pygame.font.SysFont("Arial", 30).render("You see a haunted house in the distance. What do you do?", True, (255, 255, 255))
        house_image = pygame.image.load(f"{script_dir}\house.png")
        house_image = pygame.transform.scale(house_image, (800, 300))
        button1_color = (85, 32, 48)
        button2_color = (85, 32, 48)
        button3_color = (85, 32, 48)
        button1_text = pygame.font.SysFont("Arial", 30).render("Enter House", True, (255, 255, 255))
        button2_text = pygame.font.SysFont("Arial", 30).render("Sneak In From Back", True, (255, 255, 255))
        button3_text = pygame.font.SysFont("Arial", 30).render("RUN AWAY FROM IT", True, (255, 255, 255))
        screen.fill((22, 16, 32))
        for i in range(lives):
            screen.blit(heart, (950 - (10 + i * 40), 10))
        pygame.draw.rect(screen, button1_color, button1)
        pygame.draw.rect(screen, button2_color, button2)
        pygame.draw.rect(screen, button3_color, button3)
        screen.blit(button1_text, (button1.x + 10, button1.y + 10))
        screen.blit(button2_text, (button2.x + 10, button2.y + 10))
        screen.blit(button3_text, (button3.x + 10, button3.y + 10))
        screen.blit(title, (50, 20))
        screen.blit(house_image, (100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                currentChoiceRunning = False
                running = False
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if button1.collidepoint(mouse_pos):
                    currentChoiceRunning = False
                    output = pygame.font.SysFont("Arial", 30).render("You enter the gate.", True, (255, 255, 255))
                    screen.blit(output, (50, 450))
                    pygame.display.flip()
                    time.sleep(1)
                    nextChoice = 1
                elif button2.collidepoint(mouse_pos):
                    currentChoiceRunning = False
                    output = pygame.font.SysFont("Arial", 30).render("You sneak In.", True, (255, 255, 255))
                    screen.blit(output, (50, 450))
                    pygame.display.flip()
                    time.sleep(1)
                    nextChoice = 2
                elif button3.collidepoint(mouse_pos):
                    output = pygame.font.SysFont("Arial", 30).render("Well... Nope", True, (255, 255, 255))
                    screen.blit(output, (50, 450))
                    pygame.display.flip()
                    time.sleep(0.2)
        screen.blit(output, (50, 450))
        pygame.display.flip()
    if nextChoice == 2 and lives > 0:
        currentChoiceRunning = True
        output = pygame.font.SysFont("Arial", 30).render("You can either attack spider, leave peacefully, or flip a coin.", True, (255, 255, 255))
        while currentChoiceRunning:
            title = pygame.font.SysFont("Arial", 30).render("You see a sleeping spider. What do you do?", True, (255, 255, 255))
            sleeping_spider_image = pygame.image.load(f"{script_dir}\sleeping_spider.png")
            sleeping_spider_image = pygame.transform.scale(sleeping_spider_image, (400, 300))
            button1_color = (85, 32, 48)
            button2_color = (85, 32, 48)
            button3_color = (85, 32, 48)
            button1_text = pygame.font.SysFont("Arial", 30).render("Attack Spider", True, (255, 255, 255))
            button2_text = pygame.font.SysFont("Arial", 30).render("Leave Peacefully", True, (255, 255, 255))
            button3_text = pygame.font.SysFont("Arial", 30).render("Flip A Coin", True, (255, 255, 255))
            screen.fill((22, 16, 32))
            for i in range(lives):
                screen.blit(heart, (950 - (10 + i * 40), 10))
            pygame.draw.rect(screen, button1_color, button1)
            pygame.draw.rect(screen, button2_color, button2)
            pygame.draw.rect(screen, button3_color, button3)
            screen.blit(button1_text, (button1.x + 10, button1.y + 10))
            screen.blit(button2_text, (button2.x + 10, button2.y + 10))
            screen.blit(button3_text, (button3.x + 10, button3.y + 10))
            screen.blit(title, (50, 20))
            screen.blit(sleeping_spider_image, (100, 100))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    currentChoiceRunning = False
                    running = False
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if button1.collidepoint(mouse_pos):
                        currentChoiceRunning = False
                        output = pygame.font.SysFont("Arial", 30).render("You prepare to fight the spider.", True, (255, 255, 255))
                        screen.blit(output, (50, 450))
                        pygame.display.flip()
                        time.sleep(1)
                        nextChoice = 1
                    elif button2.collidepoint(mouse_pos):
                        currentChoiceRunning = False
                        output = pygame.font.SysFont("Arial", 30).render("You leave peacefully.", True, (255, 255, 255))
                        screen.blit(output, (50, 450))
                        pygame.display.flip()
                        time.sleep(1)
                        nextChoice = 2
                    elif button3.collidepoint(mouse_pos):
                        decision = random.randint(1, 2)
                        if decision == 1:
                            currentChoiceRunning = False
                            output = pygame.font.SysFont("Arial", 30).render("You flip a coin and it lands on heads. You leave peacefully.", True, (255, 255, 255))
                            screen.blit(output, (50, 450))
                            pygame.display.flip()
                            time.sleep(1)
                            nextChoice = 2
                        else:
                            currentChoiceRunning = False
                            output = pygame.font.SysFont("Arial", 30).render("You flip a coin and it lands on tails. You prepare to fight the spider.", True, (255, 255, 255))
                            screen.blit(output, (50, 450))
                            pygame.display.flip()
                            time.sleep(1)
                            nextChoice = 1
            screen.blit(output, (50, 450))
            pygame.display.flip()
        if nextChoice == 1 and lives > 0:
            currentChoiceRunning = True
            output = pygame.font.SysFont("Arial", 30).render("You can either attack the head, back, or flip a coin.", True, (255, 255, 255))
            while currentChoiceRunning:
                title = pygame.font.SysFont("Arial", 30).render("You see a sleeping spider. What do you do?", True, (255, 255, 255))
                sleeping_spider_image = pygame.image.load(f"{script_dir}\sleeping_spider.png")
                sleeping_spider_image = pygame.transform.scale(sleeping_spider_image, (400, 300))
                button1_color = (85, 32, 48)
                button2_color = (85, 32, 48)
                button3_color = (85, 32, 48)
                button1_text = pygame.font.SysFont("Arial", 30).render("Attack The Head", True, (255, 255, 255))
                button2_text = pygame.font.SysFont("Arial", 30).render("Attack The Back", True, (255, 255, 255))
                button3_text = pygame.font.SysFont("Arial", 30).render("Flip A Coin", True, (255, 255, 255))
                screen.fill((22, 16, 32))
                for i in range(lives):
                    screen.blit(heart, (950 - (10 + i * 40), 10))
                pygame.draw.rect(screen, button1_color, button1)
                pygame.draw.rect(screen, button2_color, button2)
                pygame.draw.rect(screen, button3_color, button3)
                screen.blit(button1_text, (button1.x + 10, button1.y + 10))
                screen.blit(button2_text, (button2.x + 10, button2.y + 10))
                screen.blit(button3_text, (button3.x + 10, button3.y + 10))
                screen.blit(title, (50, 20))
                screen.blit(sleeping_spider_image, (100, 100))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        currentChoiceRunning = False
                        running = False
                        pygame.quit()
                        raise SystemExit
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = event.pos
                        if button1.collidepoint(mouse_pos):
                            currentChoiceRunning = False
                            output = pygame.font.SysFont("Arial", 30).render("You Attack The Head. The Spider Dies.", True, (255, 255, 255))
                            screen.blit(output, (50, 450))
                            pygame.display.flip()
                            time.sleep(1)
                            nextChoice = 1
                        elif button2.collidepoint(mouse_pos):
                            currentChoiceRunning = False
                            output = pygame.font.SysFont("Arial", 30).render("You Attack The Back. The Spider wakes up. You lose a life.", True, (255, 255, 255))
                            lives -= 1
                            screen.blit(output, (50, 450))
                            pygame.display.flip()
                            time.sleep(1)
                        elif button3.collidepoint(mouse_pos):
                            decision = random.randint(1, 2)
                            if decision == 1:
                                currentChoiceRunning = False
                                output = pygame.font.SysFont("Arial", 30).render("You flip a coin and it lands on heads. You attack the head. The Spider Dies.", True, (255, 255, 255))
                                screen.blit(output, (50, 450))
                                pygame.display.flip()
                                time.sleep(1)
                                nextChoice = 2
                            else:
                                currentChoiceRunning = False
                                output = pygame.font.SysFont("Arial", 30).render("You flip a coin and it lands on tails. You attack the back. The Spider wakes up. You lose a life.", True, (255, 255, 255))
                                lives -= 1
                                screen.blit(output, (50, 450))
                                pygame.display.flip()
                                time.sleep(1)
                screen.blit(output, (50, 450))
                pygame.display.flip()
    user_name = "Player"
    if lives > 0:
        currentChoiceRunning = True
        output = pygame.font.SysFont("Arial", 30).render("Tell The Ghost Your Name", True, (255, 255, 255))
        ghost_image_in_house = pygame.image.load(f"{script_dir}\ghost_in_house.png")
        ghost_image_in_house = pygame.transform.scale(ghost_image_in_house, (400, 300))
        name_box = TextBox(50, 500, 300, 40, "Enter your name...")
        while currentChoiceRunning:
            screen.fill((22, 16, 32))
            title = pygame.font.SysFont("Arial", 30).render("You see a Ghost. It asks your name.", True, (255, 255, 255))
            submit_button = pygame.Rect(370, 500, 100, 40)
            submit_button_color = (85, 32, 48)
            submit_button_text = pygame.font.SysFont("Arial", 30).render("Submit", True, (255, 255, 255))
            pygame.draw.rect(screen, submit_button_color, submit_button)
            screen.blit(submit_button_text, (submit_button.x + 10, submit_button.y + 5))
            name_box.draw(screen)
            for i in range(lives):
                screen.blit(heart, (950 - (10 + i * 40), 10))
            screen.blit(title, (50, 20))
            screen.blit(ghost_image_in_house, (100, 100))
            screen.blit(output, (50, 450))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    currentChoiceRunning = False
                    running = False
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if submit_button.collidepoint(mouse_pos):
                        entered_name = name_box.get()
                        if entered_name:
                            user_name = entered_name
                            currentChoiceRunning = False
                            output = pygame.font.SysFont("Arial", 30).render(f"You tell the ghost your name is {user_name}.", True, (255, 255, 255))
                            screen.blit(output, (50, 450))
                            pygame.display.flip()
                            time.sleep(1)
                name_box.handle_event(event)
            pygame.display.flip()
    if lives > 0:
        currentChoiceRunning = True
        output = pygame.font.SysFont("Arial", 30).render("Make your choice.", True, (255, 255, 255))
        while currentChoiceRunning:
            title = pygame.font.SysFont("Arial", 30).render(f"\"Would You Like To Play A Game {user_name}?\" The Ghost Asks.", True, (255, 255, 255))
            house_image = pygame.image.load(f"{script_dir}\house.png")
            house_image = pygame.transform.scale(house_image, (800, 300))
            button1_color = (85, 32, 48)
            button2_color = (85, 32, 48)
            button3_color = (85, 32, 48)
            button1_text = pygame.font.SysFont("Arial", 30).render("Play", True, (255, 255, 255))
            button2_text = pygame.font.SysFont("Arial", 30).render("Don't Play", True, (255, 255, 255))
            button3_text = pygame.font.SysFont("Arial", 30).render("Do Nothing", True, (255, 255, 255))
            screen.fill((22, 16, 32))
            for i in range(lives):
                screen.blit(heart, (950 - (10 + i * 40), 10))
            pygame.draw.rect(screen, button1_color, button1)
            pygame.draw.rect(screen, button2_color, button2)
            pygame.draw.rect(screen, button3_color, button3)
            screen.blit(button1_text, (button1.x + 10, button1.y + 10))
            screen.blit(button2_text, (button2.x + 10, button2.y + 10))
            screen.blit(button3_text, (button3.x + 10, button3.y + 10))
            screen.blit(title, (50, 20))
            screen.blit(house_image, (100, 100))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    currentChoiceRunning = False
                    running = False
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if button1.collidepoint(mouse_pos):
                        currentChoiceRunning = False
                        output = pygame.font.SysFont("Arial", 30).render("You play the game.", True, (255, 255, 255))
                        screen.blit(output, (50, 450))
                        pygame.display.flip()
                        time.sleep(1)
                        nextChoice = 1
                    elif button2.collidepoint(mouse_pos):
                        currentChoiceRunning = False
                        output = pygame.font.SysFont("Arial", 30).render("You don't play.", True, (255, 255, 255))
                        screen.blit(output, (50, 450))
                        pygame.display.flip()
                        time.sleep(1)
                        nextChoice = 2
                    elif button3.collidepoint(mouse_pos):
                        output = pygame.font.SysFont("Arial", 30).render("You can't stay here forever.", True, (255, 255, 255))
                        screen.blit(output, (50, 450))
                        pygame.display.flip()
                        time.sleep(0.2)
            screen.blit(output, (50, 450))
            pygame.display.flip()
    if nextChoice == 1 and lives > 0:
        for i in range(10):
            if lives <= 0:
                break
            currentChoiceRunning = True
            correct_potion = random.randint(1, 2)
            output = pygame.font.SysFont("Arial", 30).render("Choose 1 or 2", True, (255, 255, 255))
            while currentChoiceRunning:
                title = pygame.font.SysFont("Arial", 30).render("Pick A Potion", True, (255, 255, 255))
                potion_1 = pygame.image.load(f"{script_dir}\awkward_potion.png")
                potion_1 = pygame.transform.scale(potion_1, (100, 100))
                potion_2 = potion_1.copy()
                button1_color = (85, 32, 48)
                button2_color = (85, 32, 48)
                button3_color = (85, 32, 48)
                button1_text = pygame.font.SysFont("Arial", 30).render("Potion 1", True, (255, 255, 255))
                button2_text = pygame.font.SysFont("Arial", 30).render("Potion 2", True, (255, 255, 255))
                button3_text = pygame.font.SysFont("Arial", 30).render("Sit Around", True, (255, 255, 255))
                screen.fill((22, 16, 32))
                for h in range(min(lives, 5)):
                    screen.blit(heart, (950 - (h + 1) * 30, 10))
                for h in range(max(0, lives - 5)):
                    screen.blit(golden_heart, (950 - (h + 1) * 30, 40))
                pygame.draw.rect(screen, button1_color, button1)
                pygame.draw.rect(screen, button2_color, button2)
                pygame.draw.rect(screen, button3_color, button3)
                screen.blit(potion_1, (button1.centerx - 50, button1.y - 180))
                screen.blit(potion_2, (button2.centerx - 50, button2.y - 180))
                screen.blit(button1_text, (button1.x + 10, button1.y + 10))
                screen.blit(button2_text, (button2.x + 10, button2.y + 10))
                screen.blit(button3_text, (button3.x + 10, button3.y + 10))
                screen.blit(title, (50, 20))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        currentChoiceRunning = False
                        running = False
                        pygame.quit()
                        raise SystemExit
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = event.pos
                        if button1.collidepoint(mouse_pos):
                            currentChoiceRunning = False
                            if correct_potion == 1:
                                potion_1.fill((80, 255, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)
                                potion_2.fill((255, 70, 70, 255), special_flags=pygame.BLEND_RGBA_MULT)
                                output = pygame.font.SysFont("Arial", 30).render("You chose the healing potion.", True, (255, 255, 255))
                                lives += 1
                            else:
                                potion_1.fill((255, 70, 70, 255), special_flags=pygame.BLEND_RGBA_MULT)
                                potion_2.fill((80, 255, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)
                                output = pygame.font.SysFont("Arial", 30).render("You chose the harming potion.", True, (255, 255, 255))
                                lives -= 1
                            screen.blit(potion_1, (button1.centerx - 50, button1.y - 180))
                            screen.blit(potion_2, (button2.centerx - 50, button2.y - 180))
                            screen.blit(output, (50, 450))
                            pygame.display.flip()
                            time.sleep(1)
                        elif button2.collidepoint(mouse_pos):
                            currentChoiceRunning = False
                            if correct_potion == 1:
                                potion_1.fill((80, 255, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)
                                potion_2.fill((255, 70, 70, 255), special_flags=pygame.BLEND_RGBA_MULT)
                                output = pygame.font.SysFont("Arial", 30).render("You chose the harming potion.", True, (255, 255, 255))
                                lives -= 1
                            else:
                                potion_1.fill((255, 70, 70, 255), special_flags=pygame.BLEND_RGBA_MULT)
                                potion_2.fill((80, 255, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)
                                output = pygame.font.SysFont("Arial", 30).render("You chose the healing potion.", True, (255, 255, 255))
                                lives += 1
                            screen.blit(potion_1, (button1.centerx - 50, button1.y - 180))
                            screen.blit(potion_2, (button2.centerx - 50, button2.y - 180))
                            screen.blit(output, (50, 450))
                            pygame.display.flip()
                            time.sleep(1)
                        elif button3.collidepoint(mouse_pos):
                            output = pygame.font.SysFont("Arial", 30).render("Now Pick A Potion", True, (255, 255, 255))
                            screen.blit(output, (50, 450))
                            pygame.display.flip()
                            time.sleep(0.2)
                screen.blit(output, (50, 450))
                pygame.display.flip()
    if lives > 0:
        selected_riddles = random.sample(riddles, min(10, len(riddles)))
        for question, correct_answer, wrong_answer in selected_riddles:
            if lives <= 0:
                break
            riddle(question, correct_answer, wrong_answer, random.choice(["room_1.png", "room_2.png", "room_3.png"]))
    play_again_rect = pygame.Rect(360, 400, 280, 60)
    end_screen_running = True
    while end_screen_running:
        screen.fill((22, 16, 32))
        if lives <= 0:
            end_title = pygame.font.SysFont("Arial", 40).render("Game Over", True, (255, 50, 50))
        else:
            end_title = pygame.font.SysFont("Arial", 40).render("You Win!", True, (50, 255, 50))
        screen.blit(end_title, (400, 200))
        pygame.draw.rect(screen, (85, 32, 48), play_again_rect)
        btn_text = pygame.font.SysFont("Arial", 30).render("Play Again", True, (255, 255, 255))
        screen.blit(btn_text, (play_again_rect.x + 70, play_again_rect.y + 15))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_screen_running = False
                running = False
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_rect.collidepoint(event.pos):
                    end_screen_running = False
        pygame.display.flip()
pygame.quit()
