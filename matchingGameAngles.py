import pygame
import random
from math import sin
from math import cos

pygame.init()
pygame.font.init()


class Card(object):
    """ The Card Class """

    def __init__(self, left, top, width, height,
                 back_color, front_color, solved_color,
                 display,
                 font_color, text_font, value=None):
        self._width = width
        self._height = height
        self._rect = pygame.Rect(left, top, width, height)
        self._display = display
        self._back_color = back_color  # color of card when face down
        self._front_color = front_color  # color of card when face up
        self._solved_color = solved_color  # color of card after it is matched
        self._font_color = font_color
        self._text_font = text_font
        self._value = value  # the number we are trying to match
        self._unsolved = True  # is set to false once matched
        self._hidden = True  # card is face down to start
        self._times_seen = 0  # number of times player viewed card

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def times_seen(self):
        return self._times_seen

    def solved(self):
        self._unsolved = False
        pygame.draw.rect(self._display, self._solved_color, self._rect)

    def is_unsolved(self):
        return self._unsolved

    def is_clicked(self, pos):
        x_pos, y_pos = pos
        return self._rect.collidepoint(x_pos, y_pos)  # did player click on this card?

    def is_hidden(self):
        return self._hidden

    def show_card(self):
        self._hidden = False
        self._times_seen += 1
        pygame.draw.rect(self._display, self._front_color, self._rect)
        x_angle = (sin(int(self._value)) * 0.4 * min(self._width, self._height)) + self._rect.center[0]
        y_angle = (cos(int(self._value)) * 0.4 * min(self._width, self._height)) + self._rect.center[1]
        pygame.draw.circle(self._display, self._font_color,
                           self._rect.center, int(0.4 * min(self._width, self._height)), 1)
        pygame.draw.aaline(self._display, self._font_color, self._rect.center, (x_angle, y_angle))

    def hide_card(self):
        self._hidden = True
        pygame.draw.rect(self._display, self._back_color, self._rect)


def get_matching_card(card_list, card_to_match):
    """ This function returns the card that matches the one passed in """
    the_matching_card = None
    for test_card in card_list:
        if test_card.value == card_to_match.value and test_card != card_to_match:
            the_matching_card = test_card
            break
    return the_matching_card


def cards_remaining(card_list):
    """ this function returns the number of cards that have not been matched yet """
    num_remaining = 0
    for c in card_list:
        if c.is_unsolved():
            num_remaining += 1
    return num_remaining


if __name__ == "__main__":

    display_width = 600
    display_height = 600

    card_font = pygame.font.SysFont('Comic Sans MS', 48)
    front_col = pygame.Color('white')
    solved_col = pygame.Color('#636363')
    back_col = pygame.Color('#293a32')
    font_col = pygame.Color('black')

    score_font = pygame.font.SysFont('Comic Sans MS', 24)
    score_txt_col = pygame.Color('#d4c38f')
    score_y_margin = 50
    score_x_margin = 20

    player_closed_app = False
    new_game = False

    cards = []

    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Matching Game (Angles!)')
    game_display.fill(pygame.Color('#b5c9a6'))

    score_rect = pygame.draw.rect(game_display, pygame.Color('black'), pygame.Rect(0, 0, display_width, score_y_margin))

    left_pos = game_display.get_width() - score_x_margin  # replaced commented line below
    surf_4x4_txt = score_font.render("4 x 4", True, score_txt_col)
    left_pos = left_pos - surf_4x4_txt.get_width() - score_x_margin
    surf_4x4_rect = game_display.blit(surf_4x4_txt, (left_pos, (score_y_margin - surf_4x4_txt.get_height()) / 2))

    surf_sel_txt = score_font.render("Start Game:", True, score_txt_col)
    left_pos = left_pos - surf_sel_txt.get_width() - score_x_margin
    game_display.blit(surf_sel_txt, (left_pos, (score_y_margin - surf_sel_txt.get_height()) / 2))
    
    num_cols = 0
    num_rows = 0
    pick_1 = None  # variable to hold first card selected by player
    score = 0
    max_score = 0  # maximum score a player can get
    while not player_closed_app:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player_closed_app = True
        if new_game:
            pygame.draw.rect(game_display, pygame.Color('#b5c9a6'),
                             pygame.Rect(0, score_y_margin, display_width, display_height - score_y_margin))
            total_pairs = (num_cols * num_rows) / 2
            max_score = total_pairs - 1  # player gets no credit for last two cards remaining

            # create numbered pairs of angles
            pairs = []
            divs = 360 / (total_pairs + 1)
            for x in range(1, total_pairs + 1):
                pairs.append(x*divs)
                pairs.append(x*divs)

            # calculate the width and height of the cards and the space between them
            card_horz_width = int((display_width * 0.8) / num_cols)
            space_horz_width = int((display_width * 0.2) / (num_cols + 1))
            card_vert_height = int(((display_height - score_y_margin) * 0.8) / num_rows)
            space_vert_height = int(((display_height - score_y_margin) * 0.2) / (num_rows + 1))

            # create cards and randomly assign the numbered pairs
            random.random()
            del cards[:]
            for row in range(1, num_rows + 1):
                for col in range(1, num_cols + 1):
                    rnd_item = random.choice(pairs)
                    pairs.remove(rnd_item)

                    new_card_x = ((col - 1) * card_horz_width) + (col * space_horz_width)
                    new_card_y = ((row - 1) * card_vert_height) + (row * space_vert_height) + score_y_margin
                    crd = Card(new_card_x, new_card_y, card_horz_width, card_vert_height,
                               back_col, front_col, solved_col, game_display, font_col, card_font, str(rnd_item))

                    cards.append(crd)
                    crd.hide_card()

            score = 0
            new_game = False
        if pygame.mouse.get_pressed()[0]:
            if surf_4x4_rect.collidepoint(pygame.mouse.get_pos()):  # start new game 4 x 4
                new_game = True
                num_cols = 4
                num_rows = 4
                pygame.time.wait(200)  # wait 200ms to avoid multiple new game mouse click events
            for crd in cards:
                if crd.is_clicked(pygame.mouse.get_pos()) and crd.is_hidden() and crd.is_unsolved():
                    crd.show_card()
                    pygame.display.flip()
                    if pick_1 is None:
                        pick_1 = crd  # player picked first card
                    else:  # player picked second card.
                        if pick_1.value == crd.value:  # it is a match!
                            pick_1.solved()
                            crd.solved()
                            if crd.times_seen > 1 and cards_remaining(cards) > 0:
                                score += 1  # if you have seen the matching card at least once before, you get a point
                            elif crd.times_seen == 1 and cards_remaining(cards) > 0:
                                max_score -= 1  # no points for luck, we just reduce the max possible score
                            pygame.time.wait(500)  # show matching values for 500ms
                        else:  # it did not match
                            pick_1.hide_card()
                            crd.hide_card()
                            matching_card = get_matching_card(cards, pick_1)
                            if matching_card.times_seen > 0:
                                score -= 1  # player has seen the matching card before!  1 point penalty!
                            if crd.times_seen > 1:
                                score -= 1  # player should have known this card was not a match!  1 point penalty!
                            pygame.time.wait(1500)  # show card values for 1.5sec
                        pick_1 = None  # get ready for next pair of selections by player
                    break
        # update score
        surf_wrong = score_font.render("Score = " + str(score) + " out of " + str(max_score), True, score_txt_col)
        pygame.draw.rect(game_display, pygame.Color('black'),
                         pygame.Rect(score_x_margin, 0, surf_wrong.get_width() + 100, score_y_margin))
        game_display.blit(surf_wrong, (score_x_margin, (score_y_margin - surf_wrong.get_height()) / 2))
        pygame.display.flip()

    # player existed application
    pygame.quit()
    quit()
