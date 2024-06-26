from manim import *
import sympy as sym

class Cos(Scene):
    x = sym.Symbol('x')
    
    
    def polytaylor_func(fx, x0, n):
        x = Cos.x
        k = 0
        polynomial = 0
        while k <= n:
            dif = fx.diff(x, k)
            difx0 = dif.subs(x, x0)
            divisor = np.math.factorial(k)
            termk = (difx0 / divisor) * (x - x0) ** k
            polynomial = polynomial + termk
            k += 1
        return polynomial
    
    
    def construct(self):
        # self.add(NumberPlane())
        axes = Axes(
            x_range=[-5 / 2 * np.pi, 5 / 2 * np.pi, np.pi], x_length=9,
            y_range=[-2, 2, 1], y_length=4,
            tips=False)
        cos_graph = axes.plot(lambda x: np.cos(x), color=BLUE)
        
        self.play(Create(axes))
        self.wait()
        self.play(Write(cos_graph))
        self.wait()
        
        polynom4 = MathTex(r"p(x) = c_{0} + c_{1}x + c_{2}x^2 + c_{3}x^3 + c_{4}x^4", z_index=10).move_to([-3, 3.5, 0]).add_background_rectangle()
        self.play(Write(polynom4))
        self.wait()
        
        graph = VGroup(axes, cos_graph)
        self.play(graph.animate.move_to([-2.5, -2, 0]))
        self.wait()
        
        cos = MathTex(r"cos(x)").move_to([6, -1, 0])
        neg_sin = MathTex(r"-sin(x)").next_to(cos, DOWN*2+LEFT*0.5)
        neg_cos = MathTex(r"-cos(x)").next_to(neg_sin, UP*2+LEFT*0.5)
        sin = MathTex(r"sin(x)").next_to(neg_cos, UP*2+RIGHT*0.5)
        trig_functs = [cos, neg_sin, neg_cos, sin]

        arrow1 = CurvedArrow(cos.get_bottom(), neg_sin.get_right(), tip_length=0.1, angle=-TAU/4)
        arrow2 = CurvedArrow(neg_sin.get_left(), neg_cos.get_bottom(), tip_length=0.1, angle=-TAU/4)
        arrow3 = CurvedArrow(neg_cos.get_top(), sin.get_left(), tip_length=0.1, angle=-TAU/4)
        arrow4 = CurvedArrow(sin.get_right(), cos.get_top(), tip_length=0.1, angle=-TAU/4)
        arrows = [arrow1, arrow2, arrow3, arrow4]
        
        d = MathTex(r"\frac{d}{dx}").next_to(arrows[0].get_center(), DR, buff=-.05)
        d2 = MathTex(r"\frac{d}{dx}").next_to(arrows[1].get_center(), DL, buff=-.025)
        d3 = MathTex(r"\frac{d}{dx}").next_to(arrows[2].get_center(), UL, buff=-.025)
        d4 = MathTex(r"\frac{d}{dx}").next_to(arrows[3].get_center(), UR, buff=-.025)
        deriv_op = [d, d2, d3, d4]
        
        for i in range(4):
            arrows[i].set_stroke(width=2)
            deriv_op[i].set_color(YELLOW).scale(0.5)
            trig_functs[i].scale(0.8)
            self.play(Write(trig_functs[i]))
            self.wait()
            self.play(Write(arrows[i]), Write(deriv_op[i]))
            self.wait()
        
        x = sym.symbols("x")
        c0, c1, c2, c3, c4 = sym.symbols('c0 c1 c2 c3 c4')
        expr = c0 + c1 * x + c2 * x**2 + c3 * x**3 + c4 * x**4
        
        derivatives = [sym.expand(sym.diff(expr, x, i)) for i in range(6)]
        evaluated_derivatives = [deriv.subs(x, 0) for deriv in derivatives]
        derivative_tex = [
            MathTex(r"p^{(", str(i), r")}(x) = ", sym.latex(derivatives[i]))
            for i in range(6)]
        evaluated_derivative_tex = [
            MathTex(r"p^{(", str(i), r")}(0) = ", sym.latex(evaluated_derivatives[i]))
            for i in range(6)]
        
        approx_txt = [MathTex(r"cos(x) \approx "), MathTex(r"1"), MathTex(r"-0"), MathTex(r"-\frac{1}{2}x^2"), 
                      MathTex(r"+0"), MathTex(r"+\frac{1}{24}x^4"), MathTex(r"\hdots")]
        taylor_graphs = []
        for i in range(5):
            derivative_tex[i].next_to(polynom4, DOWN, aligned_edge=LEFT).add_background_rectangle().set_z_index(10)
            evaluated_derivative_tex[i].next_to(derivative_tex[i], DOWN, aligned_edge=LEFT).add_background_rectangle().set_z_index(10)
            t_i = Cos.polytaylor_func(sym.cos(Cos.x), 0, i)
            t_i_plot = axes.plot(sym.lambdify(Cos.x, t_i, modules=['numpy']), color=RED)
            taylor_graphs.append(t_i_plot)
            
            if i == 0:
                self.play(Write(derivative_tex[i]))
                self.wait()
                self.play(Write(evaluated_derivative_tex[i]))
                self.wait()
                self.play(Write(approx_txt[i].move_to([-6, 0.5, 0]).add_background_rectangle().set_z_index(10)))
                approx_txt[1].next_to(approx_txt[i]).add_background_rectangle().set_z_index(10)
                self.play(Write(approx_txt[1]), Write(taylor_graphs[i]))
                self.wait()
            else:
                approx_txt[i+1].next_to(approx_txt[i], buff=0.1).set_z_index(10)
                self.play(ReplacementTransform(derivative_tex[i-1], derivative_tex[i]))
                self.play(ReplacementTransform(evaluated_derivative_tex[i-1], evaluated_derivative_tex[i]))
                self.wait()
                self.play(Write(approx_txt[i+1].add_background_rectangle()))
                self.play(ReplacementTransform(taylor_graphs[i-1], taylor_graphs[i]))
                self.wait()
        
        approximation = VGroup(*approx_txt)
        self.play(FadeOut(derivative_tex[4], evaluated_derivative_tex[4], polynom4),
                  approximation.animate.to_edge(UL))
        
        approx_factorial = [MathTex(r"="), 
                      MathTex(r"\frac{1}{0!}x^0"), MathTex(r"-\frac{0}{1!}x^1"), MathTex(r"-\frac{1}{2!}x^2"), 
                      MathTex(r"-\frac{0}{3!}x^3"), MathTex(r"+\frac{1}{4!}x^4"), MathTex(r"\hdots")]
        approx_factorial[0].next_to(approx_txt[0], DOWN, aligned_edge=LEFT).shift(DOWN + RIGHT)
        self.play(Write(approx_factorial[0]))
        
        for i in range(1,7):
            approx_factorial[i].next_to(approx_factorial[i-1]).add_background_rectangle().set_z_index(10)
            self.play(Write(approx_factorial[i]))
            self.wait()
        
        approx_func = [MathTex(r"="), 
                      MathTex(r"\frac{cos(0)}{0!}x^0"), MathTex(r"-\frac{sin(0)}{1!}x^1"), MathTex(r"-\frac{cos(0)}{2!}x^2"), 
                      MathTex(r"+\frac{sin(0)}{3!}x^3"), MathTex(r"+\frac{cos(0)}{4!}x^4"), MathTex(r"\hdots")]
        approx_func[0].next_to(approx_factorial[0], DOWN, aligned_edge=LEFT)
        self.play(Write(approx_func[0]))
        
        for i in range(1,7):
            approx_func[i].next_to(approx_func[i-1]).add_background_rectangle().set_z_index(10)
            self.play(Write(approx_func[i]))
            self.wait()
            
        approx_taylor = [MathTex(r"="), 
                      MathTex(r"\frac{cos^{(0)}(x_0)}{0!}x^0"), MathTex(r"+\frac{cos^{(1)}(x_0)}{1!}x^1"), MathTex(r"+\frac{cos^{(2)}(x_0)}{2!}x^2"), 
                      MathTex(r"+\frac{cos^{(3)}(x_0)}{3!}x^3"), MathTex(r"+\frac{cos^{(4)}(x_0)}{4!}x^4"), MathTex(r"\hdots")]
        approx_taylor[0].next_to(approx_func[0], DOWN, aligned_edge=LEFT)
        self.play(Write(approx_taylor[0]))
        
        for i in range(1,7):
            approx_taylor[i].next_to(approx_taylor[i-1]).add_background_rectangle().set_z_index(10)
            self.play(Write(approx_taylor[i]))
            self.wait()


        
            
