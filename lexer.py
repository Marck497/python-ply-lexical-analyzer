import ply.lex as lex


palabras_reservadas = {
    "break": "BREAK",
    "do": "DO",
    "else": "ELSE",
    "float": "FLOAT",
    "for": "FOR",
    "if": "IF",
    "int": "INT",
    "while": "WHILE",
    "repeat": "KW_REPEAT",
}

tokens = tuple(palabras_reservadas.values()) + (
    "ID",
    "LIT_INT",
    "LIT_FLOAT",
    "GREATER_THAN",
    "GREATER_EQUALS",
    "LESS_THAN",
    "LESS_EQUALS",
    "EQUALS",
    "NOT_EQUALS",
    "ASSIGNMENT",
    "ADD",
    "SUBTRACT",
    "MULTIPLY",
    "DIVIDE",
    "REMAINDER",
    "AND",
    "OR",
    "NOT",
    "BITWISE_AND",
    "BITWISE_OR",
    "SEMICOLON",
    "OPEN_PARENTHESIS",
    "CLOSED_PARENTHESIS",
    "OPEN_SQUARE_BRACKET",
    "CLOSED_SQUARE_BRACKET",
    "OPEN_BRACKET",
    "CLOSED_BRACKET",
    "END_PROGRAM",
)


def t_LIT_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_LIT_INT(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_ID(t):
    r"[a-zA-Z][a-zA-Z0-9]*"
    t.type = palabras_reservadas.get(t.value, "ID")
    return t


def t_newline(t):
    r"(\r\n|\r|\n)+"
    saltos = t.value.replace("\r\n", "\n").replace("\r", "\n")
    t.lexer.lineno += len(saltos)


t_GREATER_EQUALS = r">="
t_LESS_EQUALS = r"<="
t_EQUALS = r"=="
t_NOT_EQUALS = r"!="

t_GREATER_THAN = r">"
t_LESS_THAN = r"<"

t_ASSIGNMENT = r"="

t_AND = r"&&"
t_OR = r"\|\|"
t_NOT = r"!"

t_BITWISE_AND = r"&"
t_BITWISE_OR = r"\|"

t_ADD = r"\+"
t_SUBTRACT = r"-"
t_MULTIPLY = r"\*"
t_DIVIDE = r"/"
t_REMAINDER = r"%"

t_SEMICOLON = r";"

t_OPEN_PARENTHESIS = r"\("
t_CLOSED_PARENTHESIS = r"\)"

t_OPEN_SQUARE_BRACKET = r"\["
t_CLOSED_SQUARE_BRACKET = r"\]"

t_OPEN_BRACKET = r"\{"
t_CLOSED_BRACKET = r"\}"

t_END_PROGRAM = r"\#"

t_ignore = " \t"


def find_column(input_text, lexpos):
    ultimo_n = input_text.rfind("\n", 0, lexpos)
    ultimo_r = input_text.rfind("\r", 0, lexpos)

    ultimo_salto = max(ultimo_n, ultimo_r)

    if ultimo_salto == -1:
        return lexpos + 1

    return lexpos - ultimo_salto


def t_error(t):
    columna = find_column(
        t.lexer.lexdata,
        t.lexpos,
    )

    print(
        f"Error lexico: caracter no valido "
        f"'{t.value[0]}' "
        f"en linea {t.lineno}, columna {columna}"
    )

    t.lexer.skip(1)


def formatear_token(tok):
    if tok.type == "ID":
        return f"<id, {tok.value}>"

    if tok.type == "LIT_INT":
        return f"<int, {tok.value}>"

    if tok.type == "LIT_FLOAT":
        return f"<float, {tok.value}>"

    return f"<{tok.type.lower()}>"


def analizar(input_text):
    lexer.lineno = 1
    lexer.input(input_text)

    total_componentes = 0

    while True:
        tok = lexer.token()

        if not tok:
            break

        print(formatear_token(tok))
        total_componentes += 1

        if tok.type == "END_PROGRAM":
            break

    print()
    print(f"Total componentes lexicos: {total_componentes}")
    print(f"Total lineas: {lexer.lineno}")

    return total_componentes, lexer.lineno


programa = """int contador;
float media;
int total;
int limite;
total = 0;
limite = 12;
contador = 1;
repeat (limite) {
    total = total + contador * 2;
    if (contador >= limite || total != 0) {
        media = total / 2.5;
    }
    else {
        media = 0.0;
    }
    contador = contador + 1;
}
while (contador <= limite && media != 0.0) {
    total = total % 7;
    contador = contador - 1;
}
#"""

lexer = lex.lex()

analizar(programa)
