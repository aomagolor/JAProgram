
#from lark import Lark, Transformer, v_args
import lark
# Larkのパーサーを作成
parser = lark.Lark("""
    start: program
    program: if program
         | \n
         | print program
    print: hprint
         | kprint
    ?kprint: "表示" "(" expr ")"
    ?hprint: "ひょうじ" "(" expr ")"
    ?if: "もしも" "(" shiki ")" "なら" "{" program "}" -> if
         |"もしも" "(" shiki ")" "なら" "{" program "}" "でなければ" "{" program "}" -> else
         |"もしも" "(" shiki ")" "なら" "{" program "}" "でなければもしも" "(" shiki ")" "なら" "{" program "}" -> elif
    ?shiki: expr  enzanshi  expr
    ?enzanshi: "==" -> onazi
         | "!=" -> tigau
    ?expr: term
         | expr "+" term  -> add
         | expr "-" term  -> sub
    ?term: factor
         | term "*" factor  -> mul
         | term "/" factor  -> div
    ?factor: "(" expr ")"  -> group
           | NUMBER         -> number
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
""")
def evaluate(node):
    #print(node)
    if node.data == "number":
        value = node.children[0]
        if isinstance(value, int):
            return value
        else:
            return int(value)
    elif node.data == "if":
        if node.children[0].children[1].data == "onazi":
            if evaluate(node.children[0].children[0]) == evaluate(node.children[0].children[2]):
                return evaluate(node.children[1])
        elif node.children[0].children[1].data == "tigau":
            if evaluate(node.children[0].children[0]) != evaluate(node.children[0].children[2]):
                return evaluate(node.children[1])
    elif node.data == "else":
        if node.children[0].children[1].data == "onazi":
            if evaluate(node.children[0].children[0]) == evaluate(node.children[0].children[2]):
                return evaluate(node.children[1])
            else :
                return evaluate(node.children[2])
        elif node.children[0].children[1].data == "tigau":
            if evaluate(node.children[0].children[0]) != evaluate(node.children[0].children[2]):
                return evaluate(node.children[1])
            else :
                return evaluate(node.children[2])
    elif node.data == "elif":
        if node.children[0].children[1].data == "onazi":
            if evaluate(node.children[0].children[0]) == evaluate(node.children[0].children[2]):
                return evaluate(node.children[1])
            elif node.children[2].children[1].data == "onazi":
                if evaluate(node.children[2].children[0]) == evaluate(node.children[2].children[2]):
                    return evaluate(node.cildren[3])
            elif node.children[2].children[1].data == "tigau":
                if evaluate(node.children[2].children[0]) != evaluate(node.children[2].children[2]):
                    return evaluate(node.children[3])
        elif node.children[0].children[1].data == "tigau":
            if evaluate(node.children[0].children[0]) != evaluate(node.children[0].children[2]):
                return evaluate(node.children[1])
            elif node.children[2].children[1].data == "onazi":
                if evaluate(node.children[2].children[0]) == evaluate(node.children[2].children[2]):
                    return evaluate(node.cildren[3])
            elif node.children[2].children[1].data == "tigau":
                 if evaluate(node.children[2].children[0]) != evaluate(node.children[2].children[2]):
                    return evaluate(node.cildren[3])
    elif node.data == "print":
        print(evaluate(node.children[0]))
    elif node.data == "program":
        for a in node.children:
            evaluate(a)
    elif node.data == "add":
        return evaluate(node.children[0]) + evaluate(node.children[1])
    elif node.data == "sub":
        return evaluate(node.children[0]) - evaluate(node.children[1])
    elif node.data == "mul":
        return evaluate(node.children[0]) * evaluate(node.children[1])
    elif node.data == "div":
        return evaluate(node.children[0]) / evaluate(node.children[1])
    elif node.data == "group":
        return evaluate(node.children[0])
    else:
        raise ValueError("Invalid node type: " + node.data + '\nこのエラーを見たら\nhttps://aomgolor.github.io/JAProgram/Home\nに連絡してください。')

#JAProgram = input("実行したいファイルの場所を書いてください:")
with open("JAProgramTest") as f:
    # ファイルから式を読み込み
    expr = f.read().replace("\n", "")
    # 式をパースして構文木を取得
    tree = parser.parse(expr)
    # 最上位のノードの最初の子ノードを評価して結果を出力
    #print(tree.pretty())
    evaluate(tree.children[0])