# -*- coding: utf-8 -*-

from ..actions import ForEach, DropCards, Damage, UserAction, PlayerDeath, LaunchCard, ask_for_action
from ..cards import AttackCard, Duel, Skill, TreatAs, InstantSpellCardAction, DummyCard, VirtualCard, Reject
from ..cards import t_None
from .baseclasses import register_character_to, Character
from game.autoenv import EventHandler, Game


class ReversedScales(Skill):
    associated_action = None
    skill_category = ('character', 'passive', 'compulsory')
    target = t_None


class FlowerQueen(TreatAs, Skill):
    treat_as = AttackCard
    skill_category = ('character', 'passive')

    def check(self):
        cl = self.associated_cards
        if not cl or len(cl) != 1:
            return False

        if Game.getgame().current_turn is self.player:
            return False

        return cl[0].resides_in.type in ('cards', 'showncards')


class Sadist(Skill):
    associated_action = None
    skill_category = ('character', 'passive')
    target = t_None


class ReversedScalesAction(UserAction):
    def __init__(self, target, action):
        self.source = target
        self.target = target
        self.action = action

    def apply_action(self):
        self.action.__class__ = Duel
        return True


class ReversedScalesHandler(EventHandler):
    execute_before = ('MaidenCostumeHandler', )

    def handle(self, evt_type, act):
        if evt_type != 'action_before':
            return act

        if not isinstance(act, InstantSpellCardAction):
            return act

        if isinstance(act, Reject):
            # HACK
            return act

        if ForEach.get_actual_action(act):
            return act

        src = act.source
        tgt = act.target

        if not src or tgt is src:
            return act

        if not tgt.has_skill(ReversedScales):
            return act

        g = Game.getgame()
        g.process_action(ReversedScalesAction(tgt, act))

        return act


class SadistAction(UserAction):
    def __init__(self, source, target, cards):
        self.source = source
        self.target = target
        self.cards = cards

    def apply_action(self):
        src = self.source
        tgt = self.target
        g = Game.getgame()
        g.process_action(DropCards(src, self.cards))
        g.process_action(Damage(src, tgt, 2))

        return True


class SadistHandler(EventHandler):
    card_usage = 'drop'

    def handle(self, evt_type, act):
        if evt_type != 'action_after':
            return act

        if not isinstance(act, PlayerDeath):
            return act

        src = act.source
        tgt = act.target
        g = Game.getgame()

        if not src or src is tgt:
            return act

        if not src.has_skill(Sadist):
            return act

        if g.current_turn is not src:
            return act

        dist = LaunchCard.calc_distance(tgt, DummyCard(distance=1))
        candidates = [k for k, v in dist.items() if v <= 0]

        if not candidates:
            return act

        p, rst = ask_for_action(self, [src], ('cards', 'showncards'), candidates)
        if not p:
            return act

        assert p is src

        cards, pl = rst

        g.process_action(SadistAction(src, pl[0], cards))

        return act

    def cond(self, cl):
        return len(cl) == 1 and not cl[0].is_card(VirtualCard)

    def choose_player_target(self, pl):
        return pl[-1:], len(pl)


@register_character_to('common', '-kof')
class Yuuka(Character):
    skills = [ReversedScales, FlowerQueen, Sadist]
    eventhandlers_required = [ReversedScalesHandler, SadistHandler]
    maxlife = 4
