import streamlit as st
import random

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

st.title("Tic Tac Toe")

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.score = {"You": 0, "AI": 0, "Draw": 0}


def check_winner(board):
    wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None


def update_score(result):
    if result == "x":
        st.session_state.score["You"] += 1
    elif result == "o":
        st.session_state.score["AI"] += 1
    else:
        st.session_state.score["Draw"] += 1


def ai_move():
    board = st.session_state.board
    empty = [i for i, v in enumerate(board) if v == ""]

    # AI tries to win
    for i in empty:
        board[i] = "o"
        if check_winner(board) == "o":
            return
        board[i] = ""

    # AI tries to block player
    for i in empty:
        board[i] = "x"
        if check_winner(board) == "x":
            board[i] = "o"
            return
        board[i] = ""

    if empty:
        move = random.choice(empty)
        board[move] = "o"


def handle_click(i):
    if st.session_state.board[i] == "" and not st.session_state.game_over:
        st.session_state.board[i] = "x"

        result = check_winner(st.session_state.board)
        if result:
            st.session_state.game_over = True
            update_score(result)
            return

        if not st.session_state.game_over:
            ai_move()

        result = check_winner(st.session_state.board)
        if result:
            st.session_state.game_over = True
            update_score(result)


# Game Board UI
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        st.button(
            st.session_state.board[i] if st.session_state.board[i] else " ",
            key=f"cell_{i}",
            use_container_width=True,
            on_click=handle_click,
            args=(i,),
            disabled=st.session_state.game_over or st.session_state.board[i] != ""
        )

result = check_winner(st.session_state.board)

if result:
    st.divider()
    st.markdown("## Result")
    if result == "x":
        st.metric(label="Winner", value="You", delta="+1 win")
    elif result == "o":
        st.metric(label="Winner", value="AI", delta="AI wins")
    else:
        st.metric(label="Result", value="Draw")

st.divider()
st.write("## Scoreboard")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="You", value=f"{st.session_state.score['You']}")
with col2:
    st.metric(label="AI", value=f"{st.session_state.score['AI']}")
with col3:
    st.metric(label="Draw", value=f"{st.session_state.score['Draw']}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("New Game"):
        st.session_state.board = [""] * 9
        st.session_state.game_over = False
        st.rerun()

with col2:
    if st.button("Reset Score"):
        st.session_state.score = {"You": 0, "AI": 0, "Draw": 0}
        st.rerun()