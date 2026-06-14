from manim import *
import numpy as np

class ChinesePoemEmbedding(Scene):
    def construct(self):
        self.camera.background_color = BLACK

                # ========= 代码讲解层 =========
        def show_code_overlay(
            code_text,
            title="Code",
            font_size=22,
            hold_time=2.0,
        ):
            """
            在当前画面上叠加一层半透明遮罩，并显示代码。
            退出后，原来的可视化画面继续保留。
            """

            # 1. 半透明黑色遮罩：模拟“背景虚化/退后”
            dim_layer = Rectangle(
                width=config.frame_width,
                height=config.frame_height,
                stroke_width=0,
                fill_color=BLACK,
                fill_opacity=0.72,
            )
            dim_layer.move_to(ORIGIN)
            dim_layer.set_z_index(100)

            # 2. 代码标题
            title_text = Tex(
                title,
                font_size=50,
                color=YELLOW,
            )

            # 3. 代码行（空白行用透明占位符保持布局，但不参与逐字动画）
            code_lines = VGroup()
            code_lines_with_content = []   # 只放有实际内容的行，用于逐字动画
            for line in code_text.strip("\n").split("\n"):
                if line.strip() == "":
                    # 空白行：用一个和正常行等高的透明矩形占位
                    placeholder = Rectangle(
                        width=1.0,
                        height=font_size * 0.06,   # 模拟正常行高
                        stroke_width=0,
                        fill_opacity=0,
                    )
                    code_lines.add(placeholder)
                else:
                    t = Text(
                        line,
                        font="Menlo",      # Mac 上常见；Windows 可改成 "Consolas"
                        font_size=font_size,
                        color=GREY_A,
                    )
                    code_lines.add(t)
                    code_lines_with_content.append(t)

            code_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12)

            # 如果代码太宽，就整体缩小
            if code_lines.width > 10.8:
                code_lines.scale_to_fit_width(10.8)

            # 4. 代码背景卡片（宽度取代码和标题的较大者，确保标题不超出）
            panel_width = max(code_lines.width + 0.7, title_text.width + 0.7)
            panel = RoundedRectangle(
                width=panel_width,
                height=code_lines.height + 1.5,
                corner_radius=0.12,
                stroke_color=GREY_B,
                stroke_width=1.2,
                fill_color="#111318",
                fill_opacity=0.96,
            )

            panel.move_to(ORIGIN)
            panel.set_z_index(101)

            title_text.next_to(panel.get_top(), DOWN, buff=0.18)
            title_text.align_to(panel, LEFT)
            title_text.shift(RIGHT * 0.35)
            title_text.set_z_index(102)

            code_lines.move_to(panel.get_center())
            code_lines.align_to(panel, LEFT)
            code_lines.shift(RIGHT * 0.35 + DOWN * 0.15)
            code_lines.set_z_index(102)

            overlay_group = VGroup(dim_layer, panel, title_text, code_lines)

            # 5. 进入代码讲解层
            self.play(
                FadeIn(dim_layer),
                FadeIn(panel, scale=0.98),
                FadeIn(title_text, shift=DOWN * 0.05),
                run_time=0.6,
            )

            # 6. 逐行打出代码（只动画有内容的行）
            self.play(
                LaggedStart(
                    *[AddTextLetterByLetter(line) for line in code_lines_with_content],
                    lag_ratio=0.16,
                ),
                run_time=2.2,
            )

            self.wait(hold_time)

            # 7. 退出代码讲解层
            self.play(
                FadeOut(overlay_group),
                run_time=0.6,
            )

        def show_formula_overlay(
            formula,
            title="Formula",
            hold_time=2.5,
        ):
            """
            在当前画面上叠加一层半透明遮罩，并展示 LaTeX 公式。
            formula: MathTex 或 VGroup（预排好的公式片段）
            退出后，原来的可视化画面继续保留。
            """

            # 1. 半透明黑色遮罩
            dim_layer = Rectangle(
                width=config.frame_width,
                height=config.frame_height,
                stroke_width=0,
                fill_color=BLACK,
                fill_opacity=0.72,
            )
            dim_layer.move_to(ORIGIN)
            dim_layer.set_z_index(100)

            # 2. 标题
            title_text = Tex(
                title,
                font_size=50,
                color=YELLOW,
            )

            # 3. 公式背景卡片（宽度取公式和标题的较大者，确保标题不超出）
            panel_width = max(formula.width + 1.2, title_text.width + 0.7)
            panel = RoundedRectangle(
                width=panel_width,
                height=formula.height + 1.8,
                corner_radius=0.12,
                stroke_color=GREY_B,
                stroke_width=1.2,
                fill_color="#111318",
                fill_opacity=0.96,
            )
            panel.move_to(ORIGIN)
            panel.set_z_index(101)

            title_text.next_to(panel.get_top(), DOWN, buff=0.18)
            title_text.align_to(panel, LEFT)
            title_text.shift(RIGHT * 0.35)
            title_text.set_z_index(102)

            formula.move_to(panel.get_center())
            formula.set_z_index(102)

            overlay_group = VGroup(dim_layer, panel, title_text, formula)

            # 4. 进入 overlay
            self.play(
                FadeIn(dim_layer),
                FadeIn(panel, scale=0.98),
                FadeIn(title_text, shift=DOWN * 0.05),
                run_time=0.6,
            )
            self.play(
                Write(formula),
                run_time=1.5,
            )
            self.wait(hold_time)

            # 5. 退出 overlay
            self.play(
                FadeOut(overlay_group),
                run_time=0.6,
            )

        # ========= 字体设置 =========
        # 推荐优先：
        # 1. Source Han Serif SC
        # 2. Noto Serif CJK SC
        # 如果你本机没有思源宋体，可以把下面改成 "Noto Serif CJK SC"
        chinese_font = "Source Han Serif SC"
        english_font = "CMU Serif"

        # ========= token 分词 =========
        tokens = ["春", "眠", "不", "觉", "晓", "，", "处", "处", "闻", "啼", "鸟", "↵"]

        box_colors = [
            "#0D445E",  # 春
            "#133046",  # 眠
            "#1B3D96",  # 不
            "#21377E",  # 觉
            "#274690",  # 晓
            "#2E2E2E",  # ，
            "#1C6B3F",  # 处
            "#225335",  # 处
            "#7A4A0A",  # 闻
            "#557A22",  # 啼
            "#47621C",  # 鸟
            "#3B1361",  # ↵
        ]

        # ========= token 盒子 =========
        token_groups = VGroup()
        for tok, color in zip(tokens, box_colors):
            text = Text(
                tok,
                font=chinese_font,
                font_size=34,
                color=WHITE,
            )

            box = RoundedRectangle(
                width=max(text.width + 0.22, 0.54),
                height=0.54,
                corner_radius=0.025,
                stroke_color=GREY_A,
                stroke_width=1.8,
                fill_color=color,
                fill_opacity=0.35,
            )
            text.move_to(box.get_center())
            token_groups.add(VGroup(box, text))

        token_groups.arrange(RIGHT, buff=0.35)
        token_groups.to_edge(UP, buff=0.5)
        token_groups.shift(RIGHT * 0.5)

        # ========= Position 标签 =========
        # 往里收，不要太靠外
        position_label = Text(
            "Position",
            font=english_font,
            font_size=25,
            color=TEAL_A,
        )
        position_label.next_to(token_groups[0], LEFT, buff=0.08)
        position_label.align_to(token_groups, DOWN)
        position_label.shift(DOWN * 0.30)

        # ========= position 编号 =========
        position_nums = VGroup()
        for i, tg in enumerate(token_groups, start=1):
            num = Text(
                str(i),
                font=english_font,
                font_size=30,
                color=TEAL_A,
            )
            num.next_to(tg, DOWN, buff=0.11)
            position_nums.add(num)

        # ========= embedding 向量 =========
        # 硬编码 8 维 embedding 值
        embedding_values = [
            [ 3.8, -1.1,  7.2, -3.5,  2.4,  5.8, -2.2,  1.1],   # 春
            [ 2.6, -1.9,  6.4, -4.7,  1.6,  4.8, -3.4,  0.3],   # 眠
            [-3.1,  5.8, -0.8,  8.3, -3.1,  1.9,  6.6, -4.4],   # 不
            [-2.3,  4.8, -1.6,  7.5, -4.1,  0.9,  5.6, -5.4],   # 觉
            [ 8.1,  2.4, -5.6,  1.3,  4.7, -3.2,  0.5,  5.8],   # 晓
            [-0.3,  0.8,  0.2, -0.5, -0.1,  0.6, -0.4,  0.1],   # ，
            [ 5.1, -7.8,  4.2, -1.6,  6.3, -1.4,  7.8, -2.9],   # 处
            [ 3.9, -8.6,  3.2, -2.6,  5.3, -2.4,  6.8, -4.1],   # 处
            [-6.3, -1.7,  8.9,  5.4, -4.2,  2.8, -7.1,  1.2],   # 闻
            [ 2.2,  7.7, -2.9, -7.1,  1.4,  7.0, -0.8, -2.1],   # 啼
            [ 1.4,  6.7, -3.9, -8.1,  0.4,  6.0, -1.8, -3.1],   # 鸟
            [ 0.1, -0.2,  0.4,  0.3, -0.7, -0.9,  0.2,  0.8],   # ↵
        ]

        max_abs = 9.5
        embeddings = VGroup()

        for tg, values in zip(token_groups, embedding_values):
            values_array = np.array(values).reshape(-1, 1)

            emb = DecimalMatrix(
                values_array,
                element_to_mobject_config={
                    "num_decimal_places": 1,
                    "include_sign": True,
                    "font_size": 26,
                },
                h_buff=0.30,
                v_buff=0.6 ,
                bracket_h_buff=0.06,
                left_bracket="[",
                right_bracket="]",
            )
            for entry in emb.get_entries():
                if hasattr(entry, "get_value"):
                    v = entry.get_value()
                    alpha = min(abs(v) / max_abs, 1.0)

                    if v >= 0:
                        entry.set_color(interpolate_color(BLUE_E, BLUE_A, alpha))
                    else:
                        entry.set_color(interpolate_color(RED_E, RED_A, alpha))

            emb.next_to(tg, DOWN, buff=1.05)
            emb.match_x(tg)
            embeddings.add(emb)

        # ========= arrows =========
        arrows = VGroup()
        for num, emb in zip(position_nums, embeddings):
            arrow = Arrow(
                start=num.get_bottom() + DOWN * 0.05,
                end=emb.get_top() + UP * 0.04,
                buff=0.03,
                stroke_width=15,
                max_tip_length_to_length_ratio=0.5,
                max_stroke_width_to_length_ratio=10.0,
                color=WHITE,
            )
            arrows.add(arrow)

        # ========= 左侧 维度标注 =========
        brace = Brace(embeddings[0], LEFT, buff=0.12)
        dim_label = Text(
            "12888",
            font=english_font,
            font_size=26,
            color=YELLOW,
        )
        dim_label.next_to(brace, LEFT, buff=0.16)

        # ========= 动画 =========
        self.play(
            LaggedStart(
                *[FadeIn(tg, shift=UP * 0.2) for tg in token_groups],
                lag_ratio=0.08
            ),
            run_time=1.4,
        )

        self.play(
            FadeIn(position_label, shift=RIGHT * 0.08),
            LaggedStart(
                *[FadeIn(num, shift=DOWN * 0.08) for num in position_nums],
                lag_ratio=0.08
            ),
            run_time=1.0,
        )

        self.play(
            LaggedStart(
                *[GrowArrow(ar) for ar in arrows],
                lag_ratio=0.07
            ),
            run_time=1.2,
        )

        self.play(
            LaggedStart(
                *[FadeIn(emb, shift=DOWN * 0.12) for emb in embeddings],
                lag_ratio=0.06
            ),
            run_time=1.6,
        )

        self.play(
            GrowFromCenter(brace),
            FadeIn(dim_label, shift=LEFT * 0.12),
        )

        self.wait(2)

        # ========= 展示 embedding 查表代码 =========
        show_code_overlay(
            code_text="""
embedding = nn.Embedding(
    vocab_size= 50000, d_model
    )
""",
            title="Embedding Lookup",
            font_size=24,
            hold_time=2.2,
        )

        # 消除position label 和编号，上移箭头，并把矩阵这个实体整体 transform 为 抽象记号 E1～E12

        # Step 1: 消除 position label、编号、brace 和 dim_label
        self.play(
            FadeOut(position_label, shift=RIGHT * 0.08),
            LaggedStart(
                *[FadeOut(num, shift=DOWN * 0.08) for num in position_nums],
                lag_ratio=0.08
            ),
            FadeOut(brace),
            FadeOut(dim_label, shift=LEFT * 0.12),
            LaggedStart(
                *[FadeOut(ar, shift=UP * 0.3) for ar in arrows],
                lag_ratio=0.07
            ),
            run_time=1.0,
        )

        n = len(tokens)

        def fit_to_cell(
            mob,
            center,
            cell_width,
            cell_height,
            h_padding=0.10,
            v_padding=0.08,
        ):
            """Scale a final cell target down only when it would cross a grid line."""
            max_width = max(cell_width - h_padding, 0.01)
            max_height = max(cell_height - v_padding, 0.01)

            width_scale = max_width / mob.width if mob.width > 0 else 1.0
            height_scale = max_height / mob.height if mob.height > 0 else 1.0
            scale_factor = min(1.0, width_scale, height_scale)

            if scale_factor < 1.0:
                mob.scale(scale_factor)
            mob.move_to(center)
            return mob

        # =========================
        # 布局参数
        # =========================
        qk_shift_x = -0.30
        qk_shift_y = 0.20

        grid_left = -1.6 + qk_shift_x
        grid_right = 6.8 + qk_shift_x
        grid_top = 1.55 + qk_shift_y
        grid_bottom = -4.05 + qk_shift_y

        top_token_y = 3.55 + qk_shift_y
        left_token_right_x = -5.25 + qk_shift_x

        col_w = (grid_right - grid_left) / n
        row_h = (grid_top - grid_bottom) / n

        top_centers_x = [grid_left + (j + 0.5) * col_w for j in range(n)]
        left_centers_y = [grid_top - (i + 0.5) * row_h for i in range(n)]

        # =========================
        # 样式参数
        # =========================
        e_font_size = 20
        qk_font_size = 20
        w_font_size = 14

        qk_cell_formula_font_size = 14
        qk_cell_value_font_size = 18
        ev_cell_value_font_size = 18
        ev_cell_formula_font_size = 14
        ev_operator_font_size = 14
        ev_delta_font_size = 16

        grid_stroke = 1.1
        arrow_stroke = 5

        E_COLOR = WHITE
        Q_COLOR = YELLOW
        K_COLOR = TEAL_A
        WQ_COLOR = "#C8D63C"
        WK_COLOR = TEAL_A

        # =========================================================
        # 用 TransformFromCopy：
        # 1. 原 token_groups -> 顶部横排 token
        # 2. 原 token_groups -> 左侧竖排 token
        # 3. 原 embeddings -> 顶部横排 E_i
        # 4. 原 embeddings -> 左侧竖排 E_i
        # =========================================================

        top_token_scale = 0.44
        left_token_scale = 0.50

        # ---------- 顶部横排 token 目标 ----------
        top_tokens = VGroup()
        for j in range(n):
            cx = top_centers_x[j]
            tok = token_groups[j].copy().scale(top_token_scale)
            tok.move_to([cx, top_token_y, 0])
            top_tokens.add(tok)

        # ---------- 左侧竖排 token 目标 ----------
        left_tokens = VGroup()
        for i in range(n):
            cy = left_centers_y[i]
            tok = token_groups[i].copy().scale(left_token_scale)
            tok.move_to([0, cy, 0])
            tok.shift(RIGHT * (left_token_right_x - tok.get_right()[0]))
            left_tokens.add(tok)

        # ---------- 顶部横排 E_i 目标 ----------
        top_Es = VGroup()
        for j in range(n):
            E = MathTex(
                r"\vec{E}_{%d}" % (j + 1),
                color=E_COLOR,
                font_size=e_font_size,
            )
            E.next_to(top_tokens[j], DOWN, buff=0.25)
            E.match_x(top_tokens[j])
            top_Es.add(E)

        # ---------- 左侧竖排 E_i 目标 ----------
        left_Es = VGroup()
        for i in range(n):
            E = MathTex(
                r"\vec{E}_{%d}" % (i + 1),
                color=E_COLOR,
                font_size=e_font_size,
            )
            E.next_to(left_tokens[i], RIGHT, buff=0.8)
            left_Es.add(E)

        # =========================================================
        # TransformFromCopy 动画
        # =========================================================
        self.play(
            LaggedStart(
                *[
                    TransformFromCopy(token_groups[j], top_tokens[j])
                    for j in range(n)
                ],
                lag_ratio=0.05,
            ),
            LaggedStart(
                *[
                    TransformFromCopy(token_groups[i], left_tokens[i])
                    for i in range(n)
                ],
                lag_ratio=0.05,
            ),
            LaggedStart(
                *[
                    TransformFromCopy(embeddings[j], top_Es[j])
                    for j in range(n)
                ],
                lag_ratio=0.05,
            ),
            LaggedStart(
                *[
                    TransformFromCopy(embeddings[i], left_Es[i])
                    for i in range(n)
                ],
                lag_ratio=0.05,
            ),
            FadeOut(token_groups, shift=UP * 0.2, run_time = 0.01),
            FadeOut(embeddings, shift=DOWN * 0.2, run_time = 0.01),
            run_time=2.2,
        )

        # =========================================================
        # 顶部：补 token -> E -> W_Q -> Q
        # =========================================================
        top_arrows = VGroup()
        q_symbols = VGroup()
        wq_labels = VGroup()

        for j in range(n):
            arrow1 = Arrow(
                start=top_tokens[j].get_bottom() + DOWN * 0.02,
                end=top_Es[j].get_top() + UP * 0.02,
                buff=0.02,
                stroke_width=arrow_stroke,
                max_tip_length_to_length_ratio=0.28,
                max_stroke_width_to_length_ratio=5,
                color=WHITE,
            )

            Q = MathTex(
                r"\vec{\mathbf{Q}}_{%d}" % (j + 1),
                color=Q_COLOR,
                font_size=qk_font_size,
            )
            Q.next_to(top_Es[j], DOWN, buff=0.62)
            Q.match_x(top_Es[j])

            arrow2 = Arrow(
                start=top_Es[j].get_bottom() + DOWN * 0.03,
                end=Q.get_top() + UP * 0.02,
                buff=0.02,
                stroke_width=arrow_stroke,
                max_tip_length_to_length_ratio=0.28,
                max_stroke_width_to_length_ratio=5,
                color=WHITE,
            )

            Wq = MathTex(
                r"W_Q",
                color=WQ_COLOR,
                font_size=w_font_size,
            )
            Wq.move_to((arrow2.get_start() + arrow2.get_end()) / 2)
            Wq.shift(RIGHT * 0.18)

            top_arrows.add(arrow1, arrow2)
            q_symbols.add(Q)
            wq_labels.add(Wq)

        self.play(
            LaggedStart(*[GrowArrow(ar) for ar in top_arrows], lag_ratio=0.04),
            LaggedStart(*[FadeIn(wq) for wq in wq_labels], lag_ratio=0.04),
            LaggedStart(*[FadeIn(q, shift=DOWN * 0.08) for q in q_symbols], lag_ratio=0.04),
            run_time=1.5,
        )

        # =========================================================
        # 左侧：补 token -> E -> W_K -> K
        # =========================================================
        left_arrows = VGroup()
        k_symbols = VGroup()
        wk_labels = VGroup()

        for i in range(n):
            arrow1 = Arrow(
                start=left_tokens[i].get_right() + RIGHT * 0.02,
                end=left_Es[i].get_left() + LEFT * 0.02,
                buff=0.02,
                stroke_width=arrow_stroke,
                max_tip_length_to_length_ratio=0.28,
                max_stroke_width_to_length_ratio=5,
                color=WHITE,
            )

            K = MathTex(
                r"\vec{\mathbf{K}}_{%d}" % (i + 1),
                color=K_COLOR,
                font_size=qk_font_size,
            )
            K.next_to(left_Es[i], RIGHT, buff=0.8)

            arrow2 = Arrow(
                start=left_Es[i].get_right() + RIGHT * 0.08,
                end=K.get_left() + LEFT * 0.03,
                buff=0.02,
                stroke_width=arrow_stroke,
                max_tip_length_to_length_ratio=0.28,
                max_stroke_width_to_length_ratio=5,
                color=WHITE,
            )

            Wk = MathTex(
                r"W_K",
                color=WK_COLOR,
                font_size=w_font_size,
            )
            Wk.move_to((arrow2.get_start() + arrow2.get_end()) / 2)
            Wk.shift(UP * 0.10)

            left_arrows.add(arrow1, arrow2)
            k_symbols.add(K)
            wk_labels.add(Wk)

        self.play(
            LaggedStart(*[GrowArrow(ar) for ar in left_arrows], lag_ratio=0.04),
            LaggedStart(*[FadeIn(wk) for wk in wk_labels], lag_ratio=0.04),
            LaggedStart(*[FadeIn(k, shift=RIGHT * 0.08) for k in k_symbols], lag_ratio=0.04),
            run_time=1.5,
        )

        # =========================================================
        # Grid 网格
        # =========================================================
        h_lines = VGroup()
        for r in range(n + 1):
            y = grid_top - r * row_h
            line = Line(
                start=[-7.0 + qk_shift_x, y, 0],
                end=[7.1 + qk_shift_x, y, 0],
                stroke_color=GREY_A,
                stroke_width=grid_stroke,
            )
            h_lines.add(line)

        v_lines = VGroup()
        for c in range(n + 1):
            x = grid_left + c * col_w
            line = Line(
                start=[x, grid_bottom, 0],
                end=[x, top_token_y - 0.35, 0],
                stroke_color=GREY_A,
                stroke_width=grid_stroke,
            )
            v_lines.add(line)

        self.play(
            LaggedStart(*[Create(line) for line in h_lines], lag_ratio=0.04),
            LaggedStart(*[Create(line) for line in v_lines], lag_ratio=0.04),
            run_time=1.4,
        )

        self.wait(0.5)

        # =========================================================
        # 点积动画：每个格子显示 K_i · Q_j
        # =========================================================
        dot_products = VGroup()
        dot_product_anims = []

        for i in range(n):
            for j in range(n):
                cx = top_centers_x[j]
                cy = left_centers_y[i]
                center = np.array([cx, cy, 0])

                # 目标：格子里的 K_i
                cell_k = MathTex(
                    r"\vec{\mathbf{K}}_{%d}" % (i + 1),
                    color=K_COLOR,
                    font_size=qk_cell_formula_font_size,
                )

                # 目标：格子里的点
                cell_dot = MathTex(
                    r"\cdot",
                    color=WHITE,
                    font_size=qk_cell_formula_font_size,
                )

                # 目标：格子里的 Q_j
                cell_q = MathTex(
                    r"\vec{\mathbf{Q}}_{%d}" % (j + 1),
                    color=Q_COLOR,
                    font_size=qk_cell_formula_font_size,
                )

                # 组成一整条 K_i · Q_j
                dot_prod = VGroup(cell_k, cell_dot, cell_q)
                dot_prod.arrange(RIGHT, buff=0.06)
                fit_to_cell(dot_prod, center, col_w, row_h)

                dot_products.add(dot_prod)

                # 每个格子的动画：K 从左边复制，Q 从上面复制，点号淡入
                anim = AnimationGroup(
                    TransformFromCopy(k_symbols[i], cell_k),
                    TransformFromCopy(q_symbols[j], cell_q),
                    FadeIn(cell_dot, scale=0.8),
                    lag_ratio=0.0,
                )
                dot_product_anims.append(anim)

        self.play(
            LaggedStart(
                *dot_product_anims,
                lag_ratio=0.012,
            ),
            run_time=3.0,
        )

        self.wait(0.5)

        # =========================================================
        # 点积公式 -> 数值。数值需要染色。
        # =========================================================
        # 硬编码 12×12 点积分数矩阵（K_i · Q_j）
        dot_product_values = [
            #   春     眠     不     觉     晓     ，     处     处     闻     啼     鸟     ↵
            [ 7.2,  5.8, -1.3, -0.6,  3.1, -0.5,  2.8,  2.1,  0.9,  1.6,  0.8, -0.3],  # 春
            [ 5.8,  6.9, -0.8, -0.3,  2.4, -0.4,  1.9,  1.5,  0.7,  1.1,  0.5, -0.2],  # 眠
            [-1.3, -0.8,  7.8,  6.2,  3.8,  1.2, -0.5, -0.3,  1.8,  2.4,  2.1,  0.4],  # 不
            [-0.6, -0.3,  6.2,  7.1,  4.2,  0.9, -0.1,  0.1,  1.2,  3.1,  2.8,  0.3],  # 觉
            [ 3.1,  2.4,  3.8,  4.2,  8.9,  0.6,  2.1,  1.8,  2.6,  4.1,  3.7,  0.5],  # 晓
            [-0.5, -0.4,  1.2,  0.9,  0.6,  0.8, -0.3, -0.2,  0.4, -0.1, -0.2, -0.6],  # ，
            [ 2.8,  1.9, -0.5, -0.1,  2.1, -0.3,  8.2,  6.9,  1.4,  2.8,  2.2,  0.3],  # 处1
            [ 2.1,  1.5, -0.3,  0.1,  1.8, -0.2,  6.9,  7.5,  1.1,  2.3,  1.8,  0.2],  # 处2
            [ 0.9,  0.7,  1.8,  1.2,  2.6,  0.4,  1.4,  1.1,  7.8,  3.2,  2.9,  0.1],  # 闻
            [ 1.6,  1.1,  2.4,  3.1,  4.1, -0.1,  2.8,  2.3,  3.2,  7.4,  6.5,  0.6],  # 啼
            [ 0.8,  0.5,  2.1,  2.8,  3.7, -0.2,  2.2,  1.8,  2.9,  6.5,  6.8,  0.4],  # 鸟
            [-0.3, -0.2,  0.4,  0.3,  0.5, -0.6,  0.3,  0.2,  0.1,  0.6,  0.4,  0.9],  # ↵
        ]

        max_abs_score = 9.5
        numerical_scores = VGroup()

        for i in range(n):
            for j in range(n):
                cx = top_centers_x[j]
                cy = left_centers_y[i]

                value = dot_product_values[i][j]

                num = DecimalNumber(
                    value,
                    include_sign=True,
                    num_decimal_places=1,
                    font_size=qk_cell_value_font_size,
                )

                # 根据数值正负染蓝色或红色，透明度由绝对值大小决定
                alpha = min(abs(value) / max_abs_score, 1.0)
                if value >= 0:
                    num.set_color(interpolate_color(BLUE_E, BLUE_A, alpha))
                else:
                    num.set_color(interpolate_color(RED_E, RED_A, alpha))

                fit_to_cell(num, [cx, cy, 0], col_w, row_h)
                numerical_scores.add(num)

        

        self.play(
            LaggedStart(
                *[
                    Transform(dot_products[k], numerical_scores[k])
                    for k in range(len(dot_products))
                ],
                lag_ratio=0.012,
            ),
            run_time=3.0,
        )

        self.wait(2)

        # =========================================================
        # Attention 公式 overlay：展示 QK^T / √d_k
        # =========================================================
        f_left = MathTex(
            r"\text{Attention}(Q, K, V) = \text{softmax}\!\Big(",
            font_size=34,
            color=WHITE,
        )
        f_mid = MathTex(
            r"\frac{QK^T}{\sqrt{d_k}}",
            font_size=34,
            color=YELLOW,
        )
        f_right = MathTex(
            r"\Big) V",
            font_size=34,
            color=WHITE,
        )
        attn_formula = VGroup(f_left, f_mid, f_right)
        attn_formula.arrange(RIGHT, buff=0.12)

        show_formula_overlay(
            formula=attn_formula,
            title="Scaled Dot-Product Attention",
            hold_time=2.5,
        )

        # =========================================================
        # Softmax + Causal Mask 演示
        # 假设你前面已经定义过 show_code_overlay(...)
        # =========================================================

        def column_softmax(arr):
            """
            对每一列做 softmax。
            这里列对应 query，行对应 key。
            所以每一列是在所有 key 上归一化。
            支持 -inf。
            """
            arr = np.array(arr, dtype=float)
            out = np.zeros_like(arr, dtype=float)

            for j in range(arr.shape[1]):
                col = arr[:, j]
                finite = np.isfinite(col)

                if not np.any(finite):
                    continue

                max_val = np.max(col[finite])
                exps = np.zeros_like(col, dtype=float)
                exps[finite] = np.exp(col[finite] - max_val)
                denom = np.sum(exps)

                if denom > 0:
                    out[:, j] = exps / denom

            return out

        # ---------------------------------------------------------
        # 1. 先把当前复杂 attention 图收掉
        # ---------------------------------------------------------
        full_attention_group = VGroup(
            top_tokens, top_Es, top_arrows, q_symbols, wq_labels,
            left_tokens, left_Es, left_arrows, k_symbols, wk_labels,
        )

        used_for_transform = VGroup(
            h_lines, v_lines, dot_products
        )

        # ---------------------------------------------------------
        # 2. 新建左右两个 grid：左 raw，右 normalized
        # ---------------------------------------------------------
        shape = (n, n)
        softmax_cell_size = 0.48
        softmax_value_font_size = 15

        left_grid = VGroup(*[
            Square(side_length=softmax_cell_size)
            for _ in range(shape[0] * shape[1])
        ])
        left_grid.arrange_in_grid(*shape, buff=0)
        left_grid.to_edge(LEFT, buff=0.65)
        left_grid.set_y(-0.55)
        left_grid.set_stroke(GREY_B, 1)

        right_grid = left_grid.copy()
        right_grid.to_edge(RIGHT, buff=0.65)

        grids = VGroup(left_grid, right_grid)

        arrow = Arrow(
            start=left_grid.get_right(),
            end=right_grid.get_left(),
            buff=0.18,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.22,
            color=WHITE,
        )
        sm_label = Text(
            "softmax",
            font=english_font,
            font_size=24,
            color=WHITE,
        ).next_to(arrow, UP, buff=0.12)

        titles = VGroup(
            Text(
                "Unnormalized\nAttention Pattern",
                font=english_font,
                font_size=24,
                color=WHITE,
            ),
            Text(
                "Normalized\nAttention Pattern",
                font=english_font,
                font_size=24,
                color=WHITE,
            ),
        )
        for title, grid in zip(titles, grids):
            title.next_to(grid, UP, buff=0.28)

        # ---------------------------------------------------------
        # 3. 左边 raw values：从你当前 numerical_scores copy 过去
        # ---------------------------------------------------------
        raw_array = np.array(dot_product_values, dtype=float)

        raw_values = VGroup(
            *[
                DecimalNumber(
                    value,
                    include_sign=True,
                    num_decimal_places=1,
                    font_size=softmax_value_font_size,
                ).move_to(square)
                for square, value in zip(left_grid, raw_array.flatten())
            ]
        )

        # 和之前保持一致：按正负着色
        max_abs_score = 9.5
        for val_mob, value in zip(raw_values, raw_array.flatten()):
            alpha = min(abs(value) / max_abs_score, 1.0)
            if value >= 0:
                val_mob.set_color(interpolate_color(BLUE_E, BLUE_A, alpha))
            else:
                val_mob.set_color(interpolate_color(RED_E, RED_A, alpha))

        after_transform_group = VGroup(
            left_grid, raw_values
        )
        # 注意 numerical_scores 已经是最后显示在屏幕上的数值
        self.play(
            FadeOut(full_attention_group, shift=0.15 * UP),
            ReplacementTransform(used_for_transform, after_transform_group),
            run_time=2.0,
        )

        self.wait(1)

        # ---------------------------------------------------------
        # 4. 先做一遍“正常 softmax”
        # ---------------------------------------------------------
        normalized_array = column_softmax(raw_array)

        normalized_values = VGroup(
            *[
                DecimalNumber(
                    value,
                    include_sign=False,
                    num_decimal_places=2,
                    font_size=softmax_value_font_size,
                    color=WHITE,
                ).move_to(square)
                for square, value in zip(right_grid, normalized_array.flatten())
            ]
        )


        # 用TransformFromCopy从左边 raw 数值变到右边 normalized 数值
        self.play(
            Create(right_grid),
            GrowArrow(arrow),
            FadeIn(sm_label, shift=UP * 0.08),
            FadeIn(titles, shift=UP * 0.08),
            LaggedStart(
                *[
                    TransformFromCopy(v1.copy(), v2)
                    for v1, v2 in zip(raw_values, normalized_values)
                ],
                lag_ratio=0.15,
            ),
            run_time=2.2,
        )

        self.wait(1.0)

        # ---------------------------------------------------------
        # 5. 展示 mask 代码
        # ---------------------------------------------------------
        show_code_overlay(
            code_text="""
mask = torch.tril(torch.ones(t, t, device=x.device)).bool()
""",
            title=r"Causal mask",
            font_size=24,
            hold_time=1.8,
        )

        # ---------------------------------------------------------
        # 6. 高亮左下角（i > j）的不合法位置
        #    因为我们这里：行=i 是 key，列=j 是 query
        #    对于 query j，只能看 <= j 的 key
        #    所以 i > j 的位置要 mask 掉
        # ---------------------------------------------------------
        masked_raw_values = VGroup()
        mask_rects = VGroup()
        masked_indices = []

        for idx, value_mob in enumerate(raw_values):
            i = idx // n
            j = idx % n
            if i > j:
                masked_raw_values.add(value_mob)
                masked_indices.append(idx)
                mask_rects.add(
                    SurroundingRectangle(
                        value_mob,
                        color=RED,
                        buff=0.05,
                        stroke_width=1.8,
                    )
                )

        self.play(
            LaggedStart(
                *[Create(rect) for rect in mask_rects],
                lag_ratio=0.04,
            ),
            run_time=1.5,
        )

        # ---------------------------------------------------------
        # 7. 把对应 raw score 变成 -inf
        # ---------------------------------------------------------
        raw_array_masked = raw_array.copy()
        masked_targets = []

        for idx in masked_indices:
            i = idx // n
            j = idx % n
            raw_array_masked[i, j] = -np.inf

            neg_inf = MathTex(
                r"-\infty",
                color=RED,
                font_size=17,
            ).move_to(raw_values[idx])

            masked_targets.append((raw_values[idx], neg_inf))

        self.play(
            LaggedStart(
                *[Transform(src, tgt) for src, tgt in masked_targets],
                lag_ratio=0.04,
            ),
            FadeOut(mask_rects),
            run_time=1.5,
        )

        self.wait(0.5)

        # ---------------------------------------------------------
        # 8. 刷新右边 softmax
        # ---------------------------------------------------------
        normalized_array_masked = column_softmax(raw_array_masked)

        normalized_values_masked = VGroup(
            *[
                DecimalNumber(
                    value,
                    include_sign=False,
                    num_decimal_places=2,
                    font_size=softmax_value_font_size,
                ).move_to(square)
                for square, value in zip(right_grid, normalized_array_masked.flatten())
            ]
        )

        # 对被 mask 的位置染红，强调这些位置现在概率变成 0
        for idx, val_mob in enumerate(normalized_values_masked):
            i = idx // n
            j = idx % n
            if i > j:
                val_mob.set_color(RED)
            else:
                val_mob.set_color(WHITE)


        #利用TransformFromCopy从左边被 mask 掉的 raw 数值变到右边对应的 normalized 数值（应该是 0），同时把之前的 raw 数值淡出
        self.play(
            LaggedStart(
                FadeOut(normalized_values, shift=DOWN * 0.1),
                *[
                    TransformFromCopy(v1.copy(), v2)
                    for v1, v2 in zip(raw_values, normalized_values_masked)
                ],
                lag_ratio=0.15,
            ),
            run_time=2.2,
        )

        self.wait(2)


        # =========================================================
        # Attention × V：从 masked softmax 过渡到 Value 聚合
        # 参考 attention.py 里的：
        #   - Add values
        #   - weighted_sum_cols
        #   - Show Delta E
        # =========================================================

        value_color = "#E57A67"   # 和参考图接近的橙红色
        attn_array = normalized_array_masked.copy()

        # ---------------------------------------------------------
        # 1. 大矩阵布局（回到之前 QK 那个版式，但上面改成 attention，左边改成 V）
        # ---------------------------------------------------------
        av_shift_x = -0.25
        av_shift_y = 0.20

        av_grid_left = -3.0 + av_shift_x
        av_grid_right = 6.5 + av_shift_x
        av_grid_top = 2.35 + av_shift_y
        av_grid_bottom = -3.05 + av_shift_y

        av_top_token_y = 3.55 + av_shift_y
        av_left_token_right_x = -5.75 + av_shift_x

        av_col_w = (av_grid_right - av_grid_left) / n
        av_row_h = (av_grid_top - av_grid_bottom) / n

        av_top_centers_x = [av_grid_left + (j + 0.5) * av_col_w for j in range(n)]
        av_left_centers_y = [av_grid_top - (i + 0.5) * av_row_h for i in range(n)]

        av_top_token_scale = 0.44
        av_left_token_scale = 0.50

        # ---------------------------------------------------------
        # 2. 顶部：token -> E
        # ---------------------------------------------------------
        av_top_tokens = VGroup()
        av_top_Es = VGroup()
        av_top_arrows = VGroup()

        for j in range(n):
            cx = av_top_centers_x[j]

            tok = token_groups[j].copy().scale(av_top_token_scale)
            tok.move_to([cx, av_top_token_y, 0])
            av_top_tokens.add(tok)

            E = MathTex(
                r"\vec{E}_{%d}" % (j + 1),
                color=WHITE,
                font_size=e_font_size,
            )
            E.next_to(tok, DOWN, buff=0.50)
            E.match_x(tok)
            av_top_Es.add(E)

            arr = Arrow(
                start=tok.get_bottom() + DOWN * 0.02,
                end=E.get_top() + UP * 0.02,
                buff=0.02,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.28,
                max_stroke_width_to_length_ratio=5,
                color=WHITE,
            )
            av_top_arrows.add(arr)

        # ---------------------------------------------------------
        # 3. 左侧：token -> E -> W_V -> V
        # ---------------------------------------------------------
        av_left_tokens = VGroup()
        av_left_Es = VGroup()
        av_left_arrow1s = VGroup()
        av_left_arrow2s = VGroup()
        av_wv_labels = VGroup()
        av_v_syms = VGroup()

        for i in range(n):
            cy = av_left_centers_y[i]

            tok = token_groups[i].copy().scale(av_left_token_scale)
            tok.move_to([0, cy, 0])
            tok.shift(RIGHT * (av_left_token_right_x - tok.get_right()[0]))
            av_left_tokens.add(tok)

            E = MathTex(
                r"\vec{E}_{%d}" % (i + 1),
                color=WHITE,
                font_size=e_font_size,
            )
            E.next_to(tok, RIGHT, buff=0.50)
            av_left_Es.add(E)

            arr1 = Arrow(
                start=tok.get_right() + RIGHT * 0.02,
                end=E.get_left() + LEFT * 0.02,
                buff=0.02,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.28,
                max_stroke_width_to_length_ratio=5,
                color=WHITE,
            )
            av_left_arrow1s.add(arr1)

            Vsym = MathTex(
                r"\vec{\mathbf{V}}_{%d}" % (i + 1),
                color=value_color,
                font_size=qk_font_size,
            )
            Vsym.next_to(E, RIGHT, buff=0.80)
            av_v_syms.add(Vsym)

            arr2 = Arrow(
                start=E.get_right() + RIGHT * 0.08,
                end=Vsym.get_left() + LEFT * 0.03,
                buff=0.02,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.28,
                max_stroke_width_to_length_ratio=5,
                color=WHITE,
            )
            av_left_arrow2s.add(arr2)

            Wv = MathTex(
                r"W_V",
                color=value_color,
                font_size=w_font_size,
            )
            Wv.move_to((arr2.get_start() + arr2.get_end()) / 2)
            Wv.shift(UP * 0.10)
            av_wv_labels.add(Wv)

        # ---------------------------------------------------------
        # 4. 新的大网格
        # ---------------------------------------------------------
        av_h_lines = VGroup()
        for r in range(n + 1):
            y = av_grid_top - r * av_row_h
            line = Line(
                start=[-7.0 + av_shift_x, y, 0],
                end=[7.1 + av_shift_x, y, 0],
                stroke_color=GREY_A,
                stroke_width=1.1,
            )
            av_h_lines.add(line)

        av_v_lines = VGroup()
        for c in range(n + 1):
            x = av_grid_left + c * av_col_w
            line = Line(
                start=[x, av_grid_bottom, 0],
                end=[x, av_top_token_y - 0.35, 0],
                stroke_color=GREY_A,
                stroke_width=1.1,
            )
            av_v_lines.add(line)

        # ---------------------------------------------------------
        # 5. 大矩阵里的 attention 权重（来自 softmax 后的结果）
        # ---------------------------------------------------------
        av_weights = VGroup()
        for i in range(n):
            for j in range(n):
                value = attn_array[i, j]
                color = RED if i > j else WHITE

                mob = DecimalNumber(
                    value,
                    include_sign=False,
                    num_decimal_places=2,
                    font_size=ev_cell_value_font_size,
                    color=color,
                )
                fit_to_cell(
                    mob,
                    [av_top_centers_x[j], av_left_centers_y[i], 0],
                    av_col_w,
                    av_row_h,
                )
                av_weights.add(mob)

        # ---------------------------------------------------------
        # 6. 先把 softmax 场景里不需要的东西收掉
        #    但保留 normalized_values，拿它做平滑过渡 source
        # ---------------------------------------------------------
        softmax_context = VGroup(
            left_grid,
            raw_values,
            arrow,
            sm_label,
            titles,
        )


        self.play(
            FadeOut(softmax_context, shift=UP * 0.05),
            run_time=0.8,
        )
        # ---------------------------------------------------------
        # 8. 平滑过渡：右边 normalized softmax 矩阵 -> 大矩阵里的 attention 权重
        # ---------------------------------------------------------
        self.play(
            LaggedStart(
                *[
                    ReplacementTransform(normalized_values_masked[k], av_weights[k])
                    for k in range(len(av_weights))
                ],
                lag_ratio=0.01,
            ),
            FadeOut(right_grid, shift=UP * 0.05),
            run_time=2.0,
        )
        # ---------------------------------------------------------
        # 7. 新大矩阵的框架进场
        # ---------------------------------------------------------
        self.play(
            LaggedStart(*[FadeIn(tok, shift=UP * 0.05) for tok in av_top_tokens], lag_ratio=0.05),
            LaggedStart(*[FadeIn(E, shift=UP * 0.05) for E in av_top_Es], lag_ratio=0.05),
            LaggedStart(*[GrowArrow(ar) for ar in av_top_arrows], lag_ratio=0.05),
            LaggedStart(*[FadeIn(tok, shift=RIGHT * 0.05) for tok in av_left_tokens], lag_ratio=0.05),
            LaggedStart(*[FadeIn(E, shift=RIGHT * 0.05) for E in av_left_Es], lag_ratio=0.05),
            LaggedStart(*[GrowArrow(ar) for ar in av_left_arrow1s], lag_ratio=0.05),
            LaggedStart(*[GrowArrow(ar) for ar in av_left_arrow2s], lag_ratio=0.05),
            LaggedStart(*[FadeIn(wv) for wv in av_wv_labels], lag_ratio=0.05),
            LaggedStart(*[FadeIn(vs, shift=RIGHT * 0.05) for vs in av_v_syms], lag_ratio=0.05),
            LaggedStart(*[Create(line) for line in av_h_lines], lag_ratio=0.03),
            LaggedStart(*[Create(line) for line in av_v_lines], lag_ratio=0.03),
            run_time=2.2,
        )

        
        self.wait(0.5)

        # ---------------------------------------------------------
        # 9. 对所有列：把 attention 权重和 V_i 组合成 attention_ij * V_i
        # ---------------------------------------------------------
        all_weighted_term_anims = []
        all_weighted_v_copies = VGroup()
        all_pluses = VGroup()
        all_eqs = VGroup()
        all_delta_Es = VGroup()
        all_col_terms = []   # 保存每列的 12 个加权项，供 TransformFromCopy → ΔE
        col_last_terms = []  # 记录每列最后一个 term，用于放置 = 和 ΔE

        for j in range(n):
            col_terms = VGroup()

            for i in range(n):
                cell_index = i * n + j
                cell_center = np.array([av_top_centers_x[j], av_left_centers_y[i], 0])

                weight_target = DecimalNumber(
                    attn_array[i, j],
                    include_sign=False,
                    num_decimal_places=2,
                    font_size=ev_cell_value_font_size,
                    color=(RED if i > j else WHITE),
                )

                v_copy_target = av_v_syms[i].copy()
                v_copy_target.scale(ev_cell_formula_font_size / qk_font_size)
                all_weighted_v_copies.add(v_copy_target)

                term = VGroup(weight_target, v_copy_target)
                term.arrange(RIGHT, buff=0.04)
                fit_to_cell(term, cell_center, av_col_w, av_row_h)

                col_terms.add(term)

                all_weighted_term_anims.append(
                    AnimationGroup(
                        Transform(av_weights[cell_index], weight_target),
                        TransformFromCopy(av_v_syms[i], v_copy_target),
                        lag_ratio=0.0,
                    )
                )

            col_last_terms.append(col_terms[-1])
            all_col_terms.append(col_terms)

            # 该列的行间加号
            for i in range(n - 1):
                plus = MathTex(
                    r"+",
                    color=YELLOW,
                    font_size=ev_operator_font_size,
                )
                plus.move_to(midpoint(
                    col_terms[i].get_bottom(),
                    col_terms[i + 1].get_top(),
                ))
                all_pluses.add(plus)

            # 该列底部的 = 和 ΔE_j
            eq_down = MathTex(
                "=",
                color=YELLOW,
                font_size=ev_operator_font_size,
            )
            eq_down.rotate(PI / 2)
            eq_down.next_to(col_terms[-1], DOWN, buff=0.1)

            delta_E = MathTex(
                r"\Delta \vec{E}_{%d}" % (j + 1),
                color=YELLOW,
                font_size=ev_delta_font_size,
            )
            delta_E.next_to(eq_down, DOWN, buff=0.1)

            all_eqs.add(eq_down)
            all_delta_Es.add(delta_E)

        self.play(
            av_h_lines.animate.set_stroke(opacity=0.5),
            LaggedStart(*all_weighted_term_anims, lag_ratio=0.03),
            LaggedStart(*[FadeIn(p, scale=0.8) for p in all_pluses], lag_ratio=0.03),
            run_time=2.8,
        )

        # ---------------------------------------------------------
        # 10. 每列 12 个加权项整体汇聚成 ΔE_j
        # ---------------------------------------------------------
        delta_E_anims = []

        for j in range(n):
            col_terms = all_col_terms[j]
            delta_E_target = all_delta_Es[j]

            delta_E_anims.append(
                TransformFromCopy(
                    col_terms,
                    delta_E_target
                )
            )

        self.play(
            LaggedStart(*[FadeIn(eq, scale=0.8) for eq in all_eqs], lag_ratio=0.04),
            LaggedStart(*delta_E_anims, lag_ratio=0.06),
            run_time=1.8,
        )

        self.wait(1)

        # =========================================================
        # Attention 残差：12 组 E_i 与 ΔE_i 汇聚到通用公式
        # =========================================================
        attention_residual_title = Text(
            "Attention Residual Connection",
            font=english_font,
            font_size=52,
            color=YELLOW,
        )
        attention_residual_title.move_to(ORIGIN).shift(UP * 2.8)

        attention_residual_formula = MathTex(
            r"\vec{E}_j",
            r"+",
            r"\Delta \vec{E}_j",
            r"=",
            r"\tilde{\vec{E}}_j",
            font_size=60,
        )
        attention_residual_formula[0].set_color(WHITE)
        attention_residual_formula[1].set_color(YELLOW)
        attention_residual_formula[2].set_color(YELLOW)
        attention_residual_formula[3].set_color(WHITE)
        attention_residual_formula[4].set_color(BLUE_A)
        attention_residual_formula.move_to(ORIGIN)

        av_context_to_fade = VGroup(
            av_top_tokens,
            av_top_arrows,
            av_left_tokens,
            av_left_Es,
            av_left_arrow1s,
            av_left_arrow2s,
            av_wv_labels,
            av_v_syms,
            av_h_lines,
            av_v_lines,
            av_weights,
            all_weighted_v_copies,
            all_pluses,
            all_eqs,
        )

        self.play(
            FadeOut(av_context_to_fade, shift=DOWN * 0.05),
            FadeIn(attention_residual_title, shift=DOWN * 0.1),
            ReplacementTransform(av_top_Es, attention_residual_formula[0]),
            ReplacementTransform(all_delta_Es, attention_residual_formula[2]),
            FadeIn(attention_residual_formula[1], scale=0.8),
            FadeIn(attention_residual_formula[3], scale=0.8),
            FadeIn(attention_residual_formula[4], shift=LEFT * 0.08),
            run_time=2.0,
        )

        # 统一为一个公式对象，便于后续按相同 LaTeX 片段连续变换。
        self.remove(*attention_residual_formula)
        self.add(attention_residual_formula)

        self.play(Indicate(attention_residual_formula[4], color=BLUE_A), run_time=0.8)
        self.wait(1)

        # =========================================================
        # Pre-LN FFN：\tilde{E}_j 进入 LN_2 与 FFN，得到 ΔH_j
        # =========================================================
        ffn_input_title = Text(
            "Pre-LN Layer Normalization",
            font=english_font,
            font_size=52,
            color=YELLOW,
        )
        ffn_input_title.move_to(ORIGIN).shift(UP * 2.8)

        ffn_input_formula = MathTex(
            r"\mathrm{LN}_2\!\left(",
            r"\tilde{\vec{E}}_j",
            r"\right)",
            font_size=60,
        )
        ffn_input_formula[0].set_color(TEAL_A)
        ffn_input_formula[1].set_color(BLUE_A)
        ffn_input_formula[2].set_color(TEAL_A)
        ffn_input_formula.move_to(ORIGIN)

        self.play(
            ReplacementTransform(attention_residual_formula[4], ffn_input_formula[1]),
            FadeOut(attention_residual_formula[0]),
            FadeOut(attention_residual_formula[1]),
            FadeOut(attention_residual_formula[2]),
            FadeOut(attention_residual_formula[3]),
            FadeOut(attention_residual_title),
            FadeIn(ffn_input_title, shift=DOWN * 0.1),
            FadeIn(ffn_input_formula[0]),
            FadeIn(ffn_input_formula[2]),
            run_time=1.5,
        )
        self.remove(attention_residual_formula, *ffn_input_formula)
        self.add(ffn_input_formula)

        self.play(Indicate(ffn_input_formula[1], color=BLUE_A), run_time=0.8)
        self.wait(0.8)

        ffn_output_title = Text(
            "FFN Feed-Forward Network",
            font=english_font,
            font_size=52,
            color=YELLOW,
        )
        ffn_output_title.move_to(ORIGIN).shift(UP * 2.8)

        ffn_output_formula = MathTex(
            r"\Delta \vec{H}_j",
            r"=",
            r"\mathrm{FFN}\!\left(",
            r"\mathrm{LN}_2\!\left(",
            r"\tilde{\vec{E}}_j",
            r"\right)",
            r"\right)",
            font_size=56,
        )
        ffn_output_formula[0].set_color(ORANGE)
        ffn_output_formula[1].set_color(WHITE)
        ffn_output_formula[2].set_color(TEAL_A)
        ffn_output_formula[3].set_color(TEAL_A)
        ffn_output_formula[4].set_color(BLUE_A)
        ffn_output_formula[5].set_color(TEAL_A)
        ffn_output_formula[6].set_color(TEAL_A)
        ffn_output_formula.move_to(ORIGIN)

        self.play(
            ReplacementTransform(ffn_input_formula[1], ffn_output_formula[4]),
            FadeOut(ffn_input_formula[0]),
            FadeOut(ffn_input_formula[2]),
            FadeOut(ffn_input_title),
            FadeIn(ffn_output_title, shift=DOWN * 0.1),
            FadeIn(ffn_output_formula[0]),
            FadeIn(ffn_output_formula[1]),
            FadeIn(ffn_output_formula[2]),
            FadeIn(ffn_output_formula[3]),
            FadeIn(ffn_output_formula[5]),
            FadeIn(ffn_output_formula[6]),
            run_time=1.5,
        )
        self.remove(ffn_input_formula, *ffn_output_formula)
        self.add(ffn_output_formula)

        self.play(
            Indicate(ffn_output_formula[4], color=BLUE_A),
            Indicate(ffn_output_formula[0], color=ORANGE),
            run_time=1.0,
        )
        self.wait(1)

        # =========================================================
        # FFN 残差：\tilde{E}_j + ΔH_j -> H_j
        # =========================================================
        block_output_title = Text(
            "FFN Residual → Block Output",
            font=english_font,
            font_size=52,
            color=YELLOW,
        )
        block_output_title.move_to(ORIGIN).shift(UP * 2.8)

        block_output_formula = MathTex(
            r"\vec{H}_j",
            r"=",
            r"\tilde{\vec{E}}_j",
            r"+",
            r"\Delta \vec{H}_j",
            font_size=60,
        )
        block_output_formula[0].set_color(GREEN_A)
        block_output_formula[1].set_color(WHITE)
        block_output_formula[2].set_color(BLUE_A)
        block_output_formula[3].set_color(YELLOW)
        block_output_formula[4].set_color(ORANGE)
        block_output_formula.move_to(ORIGIN)

        self.play(
            ReplacementTransform(ffn_output_formula[4], block_output_formula[2]),
            ReplacementTransform(ffn_output_formula[0], block_output_formula[4]),
            FadeOut(ffn_output_formula[1]),
            FadeOut(ffn_output_formula[2]),
            FadeOut(ffn_output_formula[3]),
            FadeOut(ffn_output_formula[5]),
            FadeOut(ffn_output_formula[6]),
            FadeOut(ffn_output_title),
            FadeIn(block_output_title, shift=DOWN * 0.1),
            FadeIn(block_output_formula[0]),
            FadeIn(block_output_formula[1]),
            FadeIn(block_output_formula[3]),
            run_time=1.6,
        )
        self.remove(ffn_output_formula, *block_output_formula)
        self.add(block_output_formula)

        self.play(
            Indicate(block_output_formula[2], color=BLUE_A),
            Indicate(block_output_formula[4], color=ORANGE),
            run_time=1.0,
        )
        self.wait(0.8)

        self.play(Indicate(block_output_formula[0], color=GREEN_A), run_time=1.0)
        self.wait(2)
