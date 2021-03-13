from discord.ext import commands
import random


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.boards = {}

    @staticmethod
    def create_empty_board():
        return [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]

    @staticmethod
    def get_row(number):
        return 0 if number < 4 else 1 if number < 7 else 2

    @staticmethod
    def get_column(number):
        return 0 if number in [1,4,7] else 1 if number in [2,5,8] else 2

    @staticmethod
    def has_line(board, d1, d2, d3, sign):
        return board[TicTacToe.get_row(d1)][TicTacToe.get_column(d1)] is sign \
               and board[TicTacToe.get_row(d2)][TicTacToe.get_column(d2)] is sign \
               and board[TicTacToe.get_row(d3)][TicTacToe.get_column(d3)] is sign

    @staticmethod
    def check_winner(board, sign):
        return TicTacToe.has_line(board, 1, 2, 3, sign) \
               or TicTacToe.has_line(board, 4, 5, 6, sign) \
               or TicTacToe.has_line(board, 7, 8, 9, sign) \
               or TicTacToe.has_line(board, 1, 4, 7, sign) \
               or TicTacToe.has_line(board, 2, 5, 8, sign) \
               or TicTacToe.has_line(board, 3, 6, 9, sign) \
               or TicTacToe.has_line(board, 1, 5, 9, sign) \
               or TicTacToe.has_line(board, 3, 5, 7, sign)

    @staticmethod
    def is_empty_board(board):
        for row in board:
            for el in row:
                if el != "-":
                    return False
        return True

    @staticmethod
    def is_full_board(board):
        for row in board:
            for el in row:
                if el == "-":
                    return False
        return True

    @staticmethod
    async def print_board(board, ctx):
        board_string = "|".join(board[0]) + "\n" + "|".join(board[1]) + "\n" + "|".join(board[2])
        print(board_string)
        await ctx.send(board_string)

    async def reset_board(self, ctx, user):
        self.boards[user] = TicTacToe.create_empty_board()
        await ctx.send("~game reset~")

    def get_board(self, user):
        if user not in self.boards:
            self.boards[user] = self.create_empty_board()
        return self.boards[user]

    async def set_cross(self, ctx, digit):
        # user turn
        user = str(ctx.message.author)
        row = TicTacToe.get_row(digit)
        column = TicTacToe.get_column(digit)
        board = self.get_board(user)

        if "-" != board[row][column]:
            await ctx.send("already occupied spot")
            return
        board[row][column] = "X"

        await TicTacToe.print_board(board, ctx)
        user_win = TicTacToe.check_winner(board, "X")
        if user_win:
            await ctx.send("you won!")
            await self.reset_board(ctx, user)
            return
        if TicTacToe.is_full_board(board):
            await ctx.send("it is a draw!")
            await self.reset_board(ctx, user)
            return

        # bot turn
        while True:
            try_row = random.randint(0,2)
            try_column = random.randint(0,2)
            if "-" == board[try_row][try_column]:
                board[try_row][try_column] = "O"
                break
        await ctx.send("-----")
        await TicTacToe.print_board(board, ctx)
        if TicTacToe.check_winner(board, "O"):
            await ctx.send("you LOST!")
            await self.reset_board(ctx, user)
            return
        if TicTacToe.is_full_board(board): # not reachable per now...
            await ctx.send("it is a draw!")
            await self.reset_board(ctx, user)

    def has_started_game(self, user):
        return user in self.boards and not self.is_empty_board(self.boards[user])

    @commands.command()
    async def tic(self, ctx, *args):
        if len(args) >= 1 and args[0].isdigit():
            digit = int(args[0])
            if digit > 9 or digit < 1:
                await ctx.send("number must be between 1 and 9")
                return

            await self.set_cross(ctx, digit)
        else:
            await ctx.send("send a number like !tic 1")

    @commands.command()
    async def tac(self, ctx, *args):
        user = str(ctx.message.author)
        board = self.get_board(user)
        await TicTacToe.print_board(board, ctx)

        if len(args) >= 1 and args[0] == "all":
            await ctx.send(self.boards)

    @commands.command()
    async def play(self, ctx, *args):
        if len(args) >= 3 and args[0] == "tic" and args[1] == "tac" and args[2] == "toe":
            user = str(ctx.message.author)
            if self.has_started_game(user):
                await ctx.send("looks like you are already playing, play using !tic {1-9}, print board with !tac")
                return
            intro_message = "ok, I'll play tic tac toe with you 🙂\n" \
                      "choose a number between 1 and 9 like !tic 2\n" \
                      "[1] [2] [3]\n" \
                      "[4] [5] [6]\n" \
                      "[7] [8] [9]"
            await ctx.send(intro_message)
            self.get_board(user)
        else:
            await ctx.send("no u play " + " ".join(args))
            await ctx.message.add_reaction('\N{EYES}')

