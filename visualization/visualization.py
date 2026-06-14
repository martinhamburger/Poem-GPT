from __future__ import annotations

import itertools as it
import random
from typing import Sequence

import numpy as np
from manim import *


# ---------------------------------------------------------------------------
# Minimal ManimGL -> Manim Community compatibility layer
#
# The scenes below intentionally keep the structure, variable names, comments,
# and layout code of the corresponding 3b1b source sections.  These helpers
# replace project-private objects from manim_imports_ext and
# _2024.transformers.helpers so the copied framework can run in Community
# Manim.  Tune the scene code below directly as needed.
# ---------------------------------------------------------------------------

ShowCreation = Create
TexText = Tex
FlashAround = Circumscribe
VFadeIn = FadeIn


def LaggedStartMap(animation_class, group, lag_ratio=0.05, run_time=None, **kwargs):
    """ManimGL-style top-level mapping; avoids animating Arrow tips separately."""
    animations = [animation_class(mobject, **kwargs) for mobject in group]
    config = {"lag_ratio": lag_ratio}
    if run_time is not None:
        config["run_time"] = run_time
    return LaggedStart(*animations, **config)


def CountInFrom(mobject, *args, **kwargs):
    return FadeIn(mobject, **kwargs)


def FadeInFromPoint(mobject, point, **kwargs):
    return FadeIn(mobject, shift=mobject.get_center() - point, **kwargs)


def FadeOutToPoint(mobject, point, **kwargs):
    return FadeOut(mobject, shift=point - mobject.get_center(), **kwargs)


def softmax(logits, temperature=1.0):
    logits = np.asarray(logits, dtype=float)
    logits = logits - np.max(logits)
    exps = np.exp(logits / temperature)
    return exps / exps.sum()


def value_to_color(value):
    alpha = min(abs(float(value)) / 10, 1)
    colors = (BLUE_E, BLUE_B) if value >= 0 else (RED_E, RED_B)
    return interpolate_color(colors[0], colors[1], alpha)


class WeightMatrix(DecimalMatrix):
    """Community-compatible copy of transformers/helpers.py:471-521."""

    def __init__(
        self,
        values=None,
        shape=(6, 8),
        value_range=(-9.9, 9.9),
        num_decimal_places=1,
        **kwargs,
    ):
        if values is None:
            values = np.random.uniform(*value_range, size=shape)
        values = np.asarray(values)
        self.shape = values.shape
        self.value_range = value_range
        self.ellipses_row = None
        self.ellipses_col = None
        super().__init__(
            values,
            element_to_mobject_config={
                "num_decimal_places": num_decimal_places,
                "include_sign": True,
                "font_size": 24,
            },
            **kwargs,
        )
        self.reset_entry_colors()

    def reset_entry_colors(self):
        for entry in self.get_entries():
            if hasattr(entry, "get_value"):
                entry.set_color(value_to_color(entry.get_value()))
        return self


class NumericEmbedding(WeightMatrix):
    """Community-compatible copy of transformers/helpers.py:524-566."""

    def __init__(
        self,
        values=None,
        length=7,
        shape=None,
        value_range=(-9.9, 9.9),
        **kwargs,
    ):
        if values is not None:
            values = np.asarray(values)
            if values.ndim == 1:
                values = values.reshape((-1, 1))
            shape = values.shape
        if shape is None:
            shape = (length, 1)
        super().__init__(values=values, shape=shape, value_range=value_range, **kwargs)


class RandomizeMatrixEntries(Animation):
    """Community-compatible copy of transformers/helpers.py:630-648."""

    def __init__(self, matrix, **kwargs):
        self.matrix = matrix
        self.entries = matrix.get_entries()
        self.start_values = [entry.get_value() for entry in self.entries]
        self.target_values = np.random.uniform(*matrix.value_range, len(self.entries))
        super().__init__(matrix, **kwargs)

    def interpolate_mobject(self, alpha):
        for index, entry in enumerate(self.entries):
            entry.set_value(interpolate(self.start_values[index], self.target_values[index], alpha))
        self.matrix.reset_entry_colors()


class SpeechBubble(VGroup):
    """Small replacement for the 3b1b SpeechBubble helper."""

    def __init__(self, text, direction=LEFT, font_size=28):
        content = Text(text, font_size=font_size)
        body = RoundedRectangle(
            width=content.width + 0.5,
            height=content.height + 0.35,
            corner_radius=0.18,
            stroke_color=WHITE,
            fill_color=BLACK,
            fill_opacity=1,
        )
        content.move_to(body)
        tip = Triangle(fill_color=BLACK, fill_opacity=1, stroke_color=WHITE).scale(0.13)
        tip.next_to(body, direction, buff=-0.02)
        super().__init__(body, tip, content)
        self.body = body
        self.content = content
        self.tip = tip

    def move_tip_to(self, point):
        self.shift(np.asarray(point) - self.tip.get_center())
        return self

    def pin_to(self, mobject):
        return self.move_tip_to(mobject.get_center())


def break_into_words(phrase_mob):
    """Standalone replacement for embedding.py:41-43."""
    # Community Text.text strips spaces; original_text preserves them.
    words = phrase_mob.original_text.split()
    result = VGroup(*[Text(word, font=phrase_mob.font, font_size=phrase_mob.font_size) for word in words])
    result.arrange(RIGHT, buff=0.12)
    result.move_to(phrase_mob)
    return result


def get_piece_rectangles(
    phrase_pieces,
    h_buff=0.05,
    v_buff=0.1,
    fill_opacity=0.15,
    fill_color=None,
    stroke_width=1,
    stroke_color=None,
):
    """Standalone replacement for embedding.py:53-90."""
    rects = VGroup()
    for piece in phrase_pieces:
        color = random_bright_color() if fill_color is None else fill_color
        rects.add(
            SurroundingRectangle(
                piece,
                buff=0,
                color=color if stroke_color is None else stroke_color,
                stroke_width=stroke_width,
                fill_color=color,
                fill_opacity=fill_opacity,
            ).stretch_to_fit_width(piece.width + 2 * h_buff).stretch_to_fit_height(piece.height + 2 * v_buff)
        )
    return rects


def show_matrix_vector_product(scene, matrix, vector, buff=0.25):
    """Lightweight replacement for helpers.py:97-134."""
    eq = MathTex("=")
    eq.next_to(vector, RIGHT, buff=buff)
    rhs = NumericEmbedding(length=matrix.shape[0])
    rhs.match_height(vector)
    rhs.next_to(eq, RIGHT, buff=buff)
    scene.play(FadeIn(eq), FadeIn(rhs.get_brackets()))
    scene.play(TransformFromCopy(VGroup(matrix, vector), rhs), run_time=1.5)
    return eq, rhs


def make_word_strip(phrase="a fluffy blue creature roamed the verdant forest"):
    phrase_mob = Text(phrase)
    words = break_into_words(phrase_mob)
    rects = get_piece_rectangles(words)
    word_groups = VGroup(*[VGroup(rect, word) for rect, word in zip(rects, words)])
    return words, rects, word_groups


def numbered_symbols(tex, count, color=WHITE, font_size=42):
    return VGroup(
        *[MathTex(rf"{tex}_{{{n}}}", font_size=font_size, color=color) for n in range(1, count + 1)]
    )


# ---------------------------------------------------------------------------
# Scene 1
# Copied from transformers/attention.py:2083-2163
# Original class: ShowAllPossibleNextTokenPredictions
# ---------------------------------------------------------------------------


class NextTokenTrainingScene(Scene):
    def construct(self):
        # Add phrase
        phrase = Text("the fluffy blue creature roamed the verdant forest despite")
        plain_words = break_into_words(phrase)
        rects = get_piece_rectangles(plain_words)
        words = VGroup(VGroup(*pair) for pair in zip(rects, plain_words))
        words = words[:-1]
        words.to_edge(LEFT, buff=MED_LARGE_BUFF)

        next_token_box = rects[-1].copy()
        next_token_box.set_color(YELLOW)
        next_token_box.set_stroke(YELLOW, 3)
        next_token_box.next_to(words, RIGHT, buff=LARGE_BUFF)
        q_marks = MathTex("???")
        q_marks.move_to(next_token_box)
        next_token_box.add(q_marks)

        # Community Manim needs explicit boundary points for VGroup arrows.
        arrow = Arrow(words.get_right(), next_token_box.get_left(), buff=SMALL_BUFF)

        self.add(words)
        self.play(GrowArrow(arrow), FadeIn(next_token_box, shift=RIGHT))
        self.wait()

        # Set up subphrases
        scale_factor = 0.75
        v_buff = 0.4
        subphrases = VGroup(*(words[:n].copy().scale(scale_factor) for n in range(1, len(words) + 1)))
        subphrases.arrange(DOWN, buff=v_buff, aligned_edge=LEFT)
        subphrases.to_corner(UL)

        rhs = VGroup(arrow, next_token_box)
        alt_rhss = VGroup(
            *(rhs.copy().scale(scale_factor).next_to(subphrase, RIGHT, SMALL_BUFF) for subphrase in subphrases)
        )

        self.play(Transform(words, subphrases[-1]), Transform(rhs, alt_rhss[-1]))
        for n in range(len(subphrases) - 1, 0, -1):
            sp1 = subphrases[n]
            sp2 = subphrases[n - 1]
            rhs1 = alt_rhss[n]
            rhs2 = alt_rhss[n - 1]
            self.play(
                TransformFromCopy(sp1[:len(sp2)], sp2),
                TransformFromCopy(rhs1, rhs2),
                rate_func=linear,
                run_time=0.5,
            )
        self.wait()

        # Highlight two examples
        for phrase, alt_rhs in zip(subphrases, alt_rhss):
            arrow = alt_rhs[0]
            alt_rhs.remove(arrow)
            phrase.add(arrow)
            phrase.save_state()
        index = 3
        self.play(
            LaggedStart(
                FadeOut(alt_rhss),
                FadeOut(rhs),
                words.animate.set_opacity(0.25),
                subphrases[:index].animate.set_opacity(0.25),
                subphrases[index + 1:].animate.set_opacity(0.25),
                subphrases[index].animate.align_to(3 * RIGHT, RIGHT),
            )
        )
        self.wait()


# ---------------------------------------------------------------------------
# Scene 2
# Copied from AttentionPatterns sections at attention.py:13-114 and 227-258
# ---------------------------------------------------------------------------


class EmbeddingScene(Scene):
    def construct(self):
        # Add sentence
        phrase = "a fluffy blue creature roamed the verdant forest"
        words, all_rects, word_groups = make_word_strip(phrase)
        word_groups.move_to(2 * UP)
        word_mobs = VGroup(*[group[1] for group in word_groups])
        all_rects = VGroup(*[group[0] for group in word_groups])

        self.play(LaggedStartMap(FadeIn, word_mobs, shift=0.5 * UP, lag_ratio=0.15))

        # Show embeddings
        embeddings = VGroup(
            *[NumericEmbedding(length=10).set_width(0.5).next_to(rect, DOWN, buff=1.5) for rect in all_rects]
        )
        emb_arrows = VGroup(
            *[Arrow(rect.get_bottom(), embedding.get_top()).match_x(rect) for rect, embedding in zip(all_rects, embeddings)]
        )
        self.play(
            FadeIn(all_rects),
            LaggedStartMap(GrowArrow, emb_arrows),
            LaggedStartMap(FadeIn, embeddings, shift=0.5 * DOWN),
        )
        self.wait()

        # Mention dimension of embedding
        brace = Brace(embeddings[0], LEFT, buff=SMALL_BUFF)
        dim_value = Integer(12288).next_to(brace, LEFT).set_color(YELLOW)
        self.play(GrowFromCenter(brace), CountInFrom(dim_value, 0))
        self.wait()

        # Collapse vectors
        emb_syms = numbered_symbols(r"\vec{\mathbf E}", len(words), GREY_A)
        for sym, rect in zip(emb_syms, all_rects):
            sym.next_to(rect, DOWN, buff=0.75)
        self.play(
            LaggedStart(
                *[ReplacementTransform(embedding, sym) for embedding, sym in zip(embeddings, emb_syms)],
                lag_ratio=0.05,
            ),
            FadeOut(brace),
            FadeOut(dim_value),
        )

        # Preview desired updates
        emb_sym_primes = VGroup(
            *[VGroup(sym.copy(), MathTex("'").scale(0.5).next_to(sym, UR, buff=0)) for sym in emb_syms]
        )
        emb_sym_primes.shift(2 * DOWN)
        emb_sym_primes.set_color(TEAL)

        full_connections = VGroup()
        for i, sym1 in enumerate(emb_syms, start=1):
            for j, sym2 in enumerate(emb_sym_primes, start=1):
                line = Line(sym1.get_bottom(), sym2.get_top(), buff=SMALL_BUFF)
                line.set_stroke(GREY_B, width=random.random() ** 2, opacity=random.random() ** 0.25)
                if (i, j) in [(2, 4), (3, 4), (4, 4), (7, 8), (8, 8)]:
                    line.set_stroke(WHITE, width=2 + random.random(), opacity=1)
                full_connections.add(line)

        self.play(
            Create(full_connections, lag_ratio=0.01, run_time=2),
            LaggedStart(
                *[TransformFromCopy(sym1, sym2) for sym1, sym2 in zip(emb_syms, emb_sym_primes)],
                lag_ratio=0.05,
            ),
        )
        self.wait()


# ---------------------------------------------------------------------------
# Scene 3
# Copied from AttentionPatterns sections at attention.py:312-430, 542-646,
# and 1027-1074.
# ---------------------------------------------------------------------------


class QKVProjectionScene(Scene):
    def construct(self):
        words, rects, word_groups = make_word_strip()
        word_groups.to_edge(UP)
        emb_arrows = VGroup(*[Vector(0.5 * DOWN).next_to(group, DOWN) for group in word_groups])
        emb_syms = numbered_symbols(r"\vec{\mathbf E}", len(words), GREY_A)
        for sym, arrow in zip(emb_syms, emb_arrows):
            sym.next_to(arrow, DOWN, SMALL_BUFF)

        self.add(word_groups, emb_arrows, emb_syms)

        # Associate questions with vectors
        q_arrows = VGroup(*[Vector(0.75 * DOWN).next_to(sym, DOWN, SMALL_BUFF) for sym in emb_syms])
        q_syms = numbered_symbols(r"\vec{\mathbf Q}", len(words), YELLOW)
        for sym, arrow in zip(q_syms, q_arrows):
            sym.next_to(arrow, DOWN, SMALL_BUFF)
        wq_syms = VGroup(*[MathTex(r"W_Q", font_size=30, color=YELLOW).next_to(arrow, RIGHT, buff=0.1) for arrow in q_arrows])

        index = 3
        question = SpeechBubble("Any adjectives\nin front of me?")
        question.move_tip_to(word_groups[index].get_top())
        self.play(FadeIn(question), word_groups[:index].animate.set_opacity(0.25), word_groups[index + 1:].animate.set_opacity(0.25))
        self.play(GrowArrow(q_arrows[index]), FadeIn(q_syms[index]), FadeIn(wq_syms[index]))

        # Show individual matrix product
        e_vect = NumericEmbedding(length=12)
        e_vect.set_height(2.4).to_corner(DL)
        matrix = WeightMatrix(shape=(7, 12))
        matrix.match_height(e_vect)
        matrix.next_to(e_vect, LEFT)
        mat_brace = Brace(matrix, UP)
        mat_label = MathTex("W_Q").next_to(mat_brace, UP, SMALL_BUFF).set_color(YELLOW)
        self.play(FadeIn(e_vect), FadeIn(matrix), GrowFromCenter(mat_brace), FadeIn(mat_label))
        eq, rhs = show_matrix_vector_product(self, matrix, e_vect)
        self.wait()

        # Add other query vectors
        self.play(
            LaggedStartMap(GrowArrow, q_arrows),
            LaggedStartMap(FadeIn, q_syms, shift=0.1 * DOWN),
            LaggedStartMap(FadeIn, wq_syms, shift=0.1 * DOWN),
            FadeOut(question),
            word_groups.animate.set_opacity(1),
        )

        # Set up keys
        key_word_groups = word_groups.copy()
        key_word_groups.arrange(DOWN, buff=0.45, aligned_edge=RIGHT)
        key_word_groups.to_edge(LEFT).shift(2.2 * DOWN)
        key_emb_syms = emb_syms.copy()
        k_syms = numbered_symbols(r"\vec{\mathbf K}", len(words), TEAL)
        wk_arrows = VGroup()
        wk_syms = VGroup()
        for group, emb_sym, k_sym in zip(key_word_groups, key_emb_syms, k_syms):
            emb_sym.next_to(group, RIGHT, SMALL_BUFF)
            wk_arrow = Vector(0.55 * RIGHT).next_to(emb_sym, RIGHT)
            wk_sym = MathTex("W_K", font_size=24, color=TEAL).next_to(wk_arrow, UP, buff=0.05)
            k_sym.next_to(wk_arrow, RIGHT, SMALL_BUFF)
            wk_arrows.add(wk_arrow)
            wk_syms.add(wk_sym)

        self.play(
            TransformFromCopy(word_groups, key_word_groups),
            TransformFromCopy(emb_syms, key_emb_syms),
            LaggedStartMap(GrowArrow, wk_arrows),
            LaggedStartMap(FadeIn, wk_syms),
            LaggedStartMap(FadeIn, k_syms),
        )

        # Add values
        v_syms = numbered_symbols(r"\vec{\mathbf V}", len(words), RED)
        wv_syms = VGroup()
        for v_sym, wk_arrow in zip(v_syms, wk_arrows):
            v_sym.next_to(wk_arrow, RIGHT, SMALL_BUFF)
            wv_syms.add(MathTex("W_V", font_size=24, color=RED).next_to(wk_arrow, DOWN, buff=0.05))
        self.play(FadeTransform(k_syms.copy(), v_syms), FadeTransform(wk_syms.copy(), wv_syms))
        self.wait()


# ---------------------------------------------------------------------------
# Scene 4
# Copied from AttentionPatterns sections at attention.py:648-890 and 982-1004.
# ---------------------------------------------------------------------------


class AttentionGridScene(Scene):
    def construct(self):
        words, rects, word_groups = make_word_strip()
        count = len(words)

        q_syms = numbered_symbols(r"\vec{\mathbf Q}", count, YELLOW, 34)
        q_syms.arrange(RIGHT, buff=0.5).to_edge(UP)
        q_words = word_groups.copy().scale(0.55)
        for group, sym in zip(q_words, q_syms):
            group.next_to(sym, UP, SMALL_BUFF)

        k_syms = numbered_symbols(r"\vec{\mathbf K}", count, TEAL, 34)
        k_syms.arrange(DOWN, buff=0.45).to_edge(LEFT).shift(0.8 * DOWN)
        k_words = word_groups.copy().scale(0.55)
        for group, sym in zip(k_words, k_syms):
            group.next_to(sym, LEFT, SMALL_BUFF)

        # Draw grid
        h_lines = VGroup(*[Line(LEFT, RIGHT).set_width(11).next_to(k_sym, UP, buff=0.25) for k_sym in k_syms])
        h_lines.add(h_lines[-1].copy().next_to(k_syms, DOWN, buff=0.25))
        v_lines = VGroup(*[Line(UP, DOWN).set_height(6).next_to(q_sym, LEFT, buff=0.25) for q_sym in q_syms])
        v_lines.add(v_lines[-1].copy().next_to(q_syms, RIGHT, buff=0.25))
        grid_lines = VGroup(*h_lines, *v_lines).set_stroke(GREY_A, 1)

        self.play(FadeIn(q_words), FadeIn(q_syms), FadeIn(k_words), FadeIn(k_syms))
        self.play(Create(h_lines, lag_ratio=0.1), Create(v_lines, lag_ratio=0.1))

        # Take all dot products
        dot_prods = VGroup()
        dots = VGroup()
        for k_sym in k_syms:
            row = VGroup()
            for q_sym in q_syms:
                square_center = np.array([q_sym.get_x(), k_sym.get_y(), 0])
                dot = Dot(square_center).set_fill(GREY_C, 0.8)
                dot.set_width(0.1 + 0.3 * random.random())
                row.add(dot)
                dot_prod = VGroup(k_sym.copy(), MathTex(r"\cdot"), q_sym.copy())
                dot_prod.arrange(RIGHT, buff=0.1).scale(0.4).move_to(square_center)
                dot_prods.add(dot_prod)
            dots.add(row)

        self.play(LaggedStartMap(FadeIn, dot_prods, lag_ratio=0.01, run_time=3))
        self.play(FadeOut(dot_prods), LaggedStartMap(GrowFromCenter, VGroup(*it.chain(*dots)), lag_ratio=0.01))

        # Show numerical dot products
        numerical_dot_prods = VGroup(
            *[
                VGroup(
                    *[
                        DecimalNumber(np.random.uniform(-10, 10), include_sign=True, num_decimal_places=1, font_size=20).move_to(dot)
                        for dot in row
                    ]
                )
                for row in dots
            ]
        )
        numerical_dot_prods[1][3].set_value(93.0)
        numerical_dot_prods[2][3].set_value(93.4)
        self.play(FadeOut(dots), FadeIn(numerical_dot_prods))

        # Focus on creature query and adjective keys
        q_rect = SurroundingRectangle(VGroup(q_words[3], q_syms[3]), color=YELLOW)
        k_rects = VGroup(*[SurroundingRectangle(VGroup(k_words[i], k_syms[i]), color=TEAL) for i in [1, 2]])
        self.play(Create(q_rect), Create(k_rects))

        # Preview masking
        masked_values = VGroup()
        mask_rects = VGroup()
        for n, row in enumerate(numerical_dot_prods):
            for value in row[:n]:
                masked_values.add(value)
                mask_rects.add(SurroundingRectangle(value, color=RED, buff=0.08))
        self.play(Create(mask_rects, lag_ratio=0.05))
        self.play(
            LaggedStart(*[Transform(value, MathTex(r"-\infty", color=RED).move_to(value)) for value in masked_values], lag_ratio=0.05),
            FadeOut(mask_rects),
        )
        self.wait()


# ---------------------------------------------------------------------------
# Scene 5
# Copied from transformers/attention.py:2169-2256
# Original class: ShowMasking
# ---------------------------------------------------------------------------


class CausalMaskSoftmaxScene(Scene):
    def construct(self):
        # Set up two patterns
        shape = (6, 6)
        left_grid = VGroup(*[Square(0.72) for _ in range(shape[0] * shape[1])])
        left_grid.arrange_in_grid(*shape, buff=0)
        left_grid.to_edge(LEFT)
        left_grid.set_y(-0.5)
        left_grid.set_stroke(GREY_B, 1)

        right_grid = left_grid.copy()
        right_grid.to_edge(RIGHT)

        grids = VGroup(left_grid, right_grid)
        arrow = Arrow(left_grid.get_right(), right_grid.get_left())
        sm_label = Text("softmax").next_to(arrow, UP)

        titles = VGroup(Text("Unnormalized\nAttention Pattern"), Text("Normalized\nAttention Pattern"))
        for title, grid in zip(titles, grids):
            title.next_to(grid, UP, buff=MED_LARGE_BUFF)

        values_array = np.random.normal(0, 2, shape)
        raw_values = VGroup(
            *[
                DecimalNumber(value, include_sign=True, font_size=25).move_to(square)
                for square, value in zip(left_grid, values_array.flatten())
            ]
        )

        self.add(left_grid, right_grid, titles, arrow, sm_label, raw_values)

        # Highlight lower lefts
        changers = VGroup()
        for n, dec in enumerate(raw_values):
            i = n // shape[1]
            j = n % shape[1]
            if i > j:
                changers.add(dec)
                dec.target = MathTex(r"-\infty", font_size=30, color=RED).move_to(dec)
                values_array[i, j] = -np.inf
        rects = VGroup(*[SurroundingRectangle(changer, color=RED) for changer in changers])
        self.play(LaggedStartMap(Create, rects))
        self.play(LaggedStartMap(FadeOut, rects), LaggedStartMap(MoveToTarget, changers))
        self.wait()

        # Normalized values
        normalized_array = np.array([softmax(col) for col in values_array.T]).T
        normalized_values = VGroup(
            *[
                DecimalNumber(value, font_size=25).move_to(square)
                for square, value in zip(right_grid, normalized_array.flatten())
            ]
        )
        for n, value in enumerate(normalized_values):
            if (n // shape[1]) > (n % shape[1]):
                value.set_color(RED)
        self.play(
            LaggedStart(
                *[FadeTransform(v1.copy(), v2) for v1, v2 in zip(raw_values, normalized_values)],
                lag_ratio=0.05,
            )
        )
        self.wait()


# ---------------------------------------------------------------------------
# Scene 6
# Copied from AttentionPatterns sections at attention.py:1027-1157 and
# IntroduceValueMatrix at attention.py:2416-2477.
# ---------------------------------------------------------------------------


class ValueAggregationScene(Scene):
    def construct(self):
        words, rects, word_groups = make_word_strip()
        word_groups.to_edge(LEFT).shift(2.2 * UP)
        index = 3

        # Add values
        value_color = RED
        big_wv_sym = MathTex(r"W_V", font_size=90, color=value_color)
        big_wv_sym.to_corner(DL)
        wv_word = Text("Value matrix", font_size=50, color=value_color).next_to(big_wv_sym, UP)

        matrix = WeightMatrix(shape=(8, 8))
        matrix.set_height(2.75).to_corner(DL)
        matrix_brace = Brace(matrix, UP)
        matrix_label = MathTex("W_V", color=RED).next_to(matrix_brace, UP)

        embeddings = VGroup(*[NumericEmbedding(length=8).set_height(2.5) for _ in words])
        embeddings.arrange(RIGHT, buff=0.45).next_to(word_groups, DOWN, buff=0.6)
        emb_arrows = VGroup(*[Arrow(group.get_bottom(), emb.get_top(), buff=0.1) for group, emb in zip(word_groups, embeddings)])
        self.add(word_groups)
        self.play(LaggedStartMap(GrowArrow, emb_arrows), LaggedStartMap(FadeIn, embeddings))

        # Show value matrix product
        fluff_emb = embeddings[1]
        in_vect_rect = SurroundingRectangle(fluff_emb, color=TEAL)
        in_vect = fluff_emb.copy().match_height(matrix).next_to(matrix, RIGHT, SMALL_BUFF)
        self.play(FadeIn(matrix), GrowFromCenter(matrix_brace), FadeIn(matrix_label))
        self.play(Create(in_vect_rect), TransformFromCopy(fluff_emb, in_vect))
        eq, rhs = show_matrix_vector_product(self, matrix, in_vect)

        value_rect = SurroundingRectangle(rhs, color=RED)
        value_label = Text("Value", color=RED).next_to(value_rect, RIGHT)
        self.play(Create(value_rect), FadeIn(value_label))

        # Show column of weights
        v_syms = numbered_symbols(r"\vec{\mathbf V}", len(words), RED, 34)
        v_syms.arrange(DOWN, buff=0.4).to_edge(LEFT).shift(0.6 * DOWN)
        weights = softmax([0.1, 3.0, 3.2, 0.4, -0.5, -1.0, -1.2, -1.4])
        softmax_col = VGroup(*[DecimalNumber(value, num_decimal_places=2, font_size=28) for value in weights])
        softmax_col.arrange(DOWN, buff=0.42).next_to(v_syms, RIGHT, buff=0.4)
        self.play(FadeIn(v_syms), FadeIn(softmax_col))

        weighted_sum_col = VGroup()
        for weight, v_sym in zip(softmax_col, v_syms):
            product = VGroup(weight.copy(), v_sym.copy()).arrange(RIGHT)
            product.move_to(weight)
            weighted_sum_col.add(product)
        self.play(LaggedStartMap(FadeIn, weighted_sum_col))

        # Emphasize fluffy and blue weights
        rects = VGroup(*[SurroundingRectangle(softmax_col[i], color=TEAL) for i in [1, 2]])
        self.play(Create(rects))

        # Show sum
        plusses = VGroup()
        for m1, m2 in zip(weighted_sum_col, weighted_sum_col[1:]):
            plusses.add(MathTex("+").move_to(midpoint(m1.get_bottom(), m2.get_top())))
        result = MathTex(r"\Delta E_4", color=TEAL, font_size=52).next_to(weighted_sum_col, RIGHT, buff=1.0)
        equals = MathTex("=", font_size=52).next_to(result, LEFT)
        self.play(FadeIn(plusses), FadeIn(equals), FadeTransform(weighted_sum_col.copy(), result))
        self.wait()
