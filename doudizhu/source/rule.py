from collections import Counter
import logging
import json

'''
# A 2 3 4 5 6 7 8 9 0 J Q K W w
# 记分
# 地主先出完所有的牌就赢了，如果没有出过炸弹或火箭，那么每个农民要把定约的分数(1分、2分或3分)付给地主。
# 两个农民中有一个先出完所有的牌，地主就输了，那么地主要把定约的分数付给每个农民。
# 每当任何一个玩家出了炸弹或火箭，那么分数就要翻一番。
# 例如某局牌出了2个炸弹和1个火箭，叫3分的地主如果先出完，他就向每个农民赢得24分【总共赢得48分】，
# 如果农民先出完，地主就向每个农民输掉24分【总共输掉48分】。
'''

CARD_TYPES = [
    # 'rocket', 'bomb',
    'single', 'pair', 'trio', 'trio_pair', 'trio_single',
    'seq_single5', 'seq_single6', 'seq_single7', 'seq_single8', 'seq_single9', 'seq_single10', 'seq_single11',
    'seq_single12',
    'seq_pair3', 'seq_pair4', 'seq_pair5', 'seq_pair6', 'seq_pair7', 'seq_pair8', 'seq_pair9', 'seq_pair10',
    'seq_trio2', 'seq_trio3', 'seq_trio4', 'seq_trio5', 'seq_trio6',
    'seq_trio_pair2', 'seq_trio_pair3', 'seq_trio_pair4', 'seq_trio_pair5',
    'seq_trio_single2', 'seq_trio_single3', 'seq_trio_single4', 'seq_trio_single5',
    'bomb_pair', 'bomb_single'
]


class Rule(object):

    def __init__(self, rules):
        self.rules = rules

    @staticmethod
    def is_contains(parent, child):
        parent, child = Counter(parent), Counter(child)
        for k, n in child.items():
            if k not in parent or n > parent[k]:
                return False
        return True

    def cards_above(self, hand_pokers, turn_pokers):
        if turn_pokers == []:
            return [hand_pokers[0]]
        hand_cards = self._to_cards(hand_pokers)
        turn_cards = self._to_cards(turn_pokers)

        card_type, card_value = self._cards_value(turn_cards)
        if not card_type:
            return []
        one_rule = self.rules[card_type]
        for i, t in enumerate(one_rule):
            if i > card_value and self.is_contains(hand_cards, t):
                return self._to_pokers(hand_pokers, t)

        if card_value < 2000:
            one_rule = self.rules['bomb']
            for t in one_rule:
                if self.is_contains(hand_cards, t):
                    return self._to_pokers(hand_pokers, t)
            if self.is_contains(hand_cards, 'wW'):
                return [53, 54]
        return []

    @staticmethod
    def _to_cards(pokers):
        cards = []
        for p in pokers:
            p-=1
            if p == 52:
                cards.append('w')
            elif p == 53:
                cards.append('W')
            else:
                cards.append('34567890JQKA2'[int(p/4)])
        return Rule._sort_card(cards)

    @staticmethod
    def _to_poker(card):
        if card == 'W':
            return [54]
        if card == 'w':
            return [53]

        cards = '34567890JQKA2'
        for i, c in enumerate(cards):
            if c == card:
                return [i*4+1, i*4+2, i*4+3, i*4+4]
        return [55]

    @staticmethod
    def _to_pokers(hand_pokers, cards):
        pokers = []
        for card in cards:
            candidates = Rule._to_poker(card)
            for cd in candidates:
                if cd in hand_pokers and cd not in pokers:
                    pokers.append(cd)
                    break
        return pokers

    def _cards_value(self, cards):
        cards = ''.join(cards)
        if cards == 'wW':
            return 'rocket', 2000

        value = self._index_of(self.rules['bomb'], cards)
        if value >= 0:
            return 'bomb', 1000 + value

        return self._card_type(cards)

    def compare_poker(self, a_pokers, b_pokers):
        if not a_pokers or not b_pokers:
            if a_pokers == b_pokers:
                return 0
            if a_pokers:
                return 1
            if b_pokers:
                return 1

        a_card_type, a_card_value = self._cards_value(self._to_cards(a_pokers))
        b_card_type, b_card_value = self._cards_value(self._to_cards(b_pokers))
        if a_card_type == b_card_type:
            return a_card_value - b_card_value

        if a_card_value >= 1000:
            return 1
        else:
            return 0

    def _card_type(self, cards):
        for t in CARD_TYPES:
            value = self._index_of(self.rules[t], cards)
            if value >= 0:
                return t, value
        logging.error('Unknown Card Type: %s', cards)
        # raise Exception('Unknown Card Type: %s' % cards)
        return '', 0

    @staticmethod
    def _sort_card(cards):
        cards.sort(key=lambda ch: '34567890JQKA2wW'.index(ch))
        return cards

    @staticmethod
    def _index_of(array, ele):
        if len(array[0]) != len(ele):
            return -1
        for i, e in enumerate(array):
            if e == ele:
                return i
        return -1


with open('rule.json', 'r') as f:
    rule = Rule(json.load(f))
