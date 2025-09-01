import string

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'encryption'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    LOOKUP_TABLES = [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBA",
        "FEDCBAGHIJKLMZYXWVUTSRQPON",
    ]


class Subsession(BaseSubsession):
    payment_per_correct = models.CurrencyField()
    lookup_table = models.StringField()
    word = models.StringField()

    def setup_round(self):
        self.payment_per_correct = Currency(0.10)
        self.lookup_table = C.LOOKUP_TABLES[(self.round_number-1) % 3]
        self.word = "ABABA"

    @property
    def lookup_dict(self):
        lookup = {}
        for letter in string.ascii_uppercase:
            lookup[letter] = self.lookup_table.index(letter)+1
        return lookup

    @property
    def correct_response(self):
        return [self.lookup_dict[letter] for letter in self.word]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    response_1 = models.IntegerField()
    response_2 = models.IntegerField()
    response_3 = models.IntegerField()
    response_4 = models.IntegerField()
    response_5 = models.IntegerField()
    is_correct = models.BooleanField()

    @property
    def response_fields(self):
        return [
            "response_1",
            "response_2",
            "response_3",
            "response_4",
            "response_5",
        ]

    @property
    def response(self):
        return [
            self.response_1,
            self.response_2,
            self.response_3,
            self.response_4,
            self.response_5,
        ]

    def check_response(self):
        self.is_correct = self.response == self.subsession.correct_response
        if self.is_correct:
            self.payoff = self.subsession.payment_per_correct


def creating_session(subsession):
    subsession.setup_round()


# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Decision(Page):
    form_model = "player"

    @staticmethod
    def get_form_fields(player):
        return player.response_fields

    def before_next_page(player, timeout_happened):
        player.check_response()


class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    Intro,
    Decision,
    Results,
]
