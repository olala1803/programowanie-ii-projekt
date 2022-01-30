import asyncio
import discord
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_TOKEN")


class DiscordBotClient(discord.Client):

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(client))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        if message.content.startswith('$games'):
            await message.channel.send('Games: hangman, rockpaperscissors (rps), guess the dice (type: $hangman / $rps / $dice )')

        # Hangman
        if message.content.startswith('$hangman'):
            await message.channel.send("Let's play hangman! Please select difficulty level (easy / hard)")

            def is_correct(m):
                return m.author == message.author

            def is_correct_letter(m):
                return m.author == message.author and len(m.content) == 1

            try:
                lvl = await self.wait_for('message', check=is_correct, timeout=20.0)
            except asyncio.TimeoutError:
                return await message.channel.send('Sorry, time for the answer has ended!')

            if lvl.content == 'easy':
                await message.channel.send("You've picked easy level!")

                words = ['city', 'cube', 'shop', 'sick', 'when']
                word = random.choice(words)
                word_ = '----'
                guess = 0

                lifes = 10

                while(lifes >= 0 and guess != 4):
                    await message.channel.send("Word: {}".format(word_))
                    await message.channel.send("Guess letter! Your lifes: {}".format(lifes))

                    try:
                        ans = await self.wait_for('message', check=is_correct_letter, timeout=20.0)
                    except asyncio.TimeoutError:
                        return await message.channel.send('Sorry, time for the answer has ended!')

                    if ans.content in word:
                        await message.channel.send("Goodjob! you guessed letter: {}!".format(ans.content))
                        c = ''
                        for i in range(len(word_)):
                            if i == word.index(ans.content):
                                c = c + ans.content
                            elif word_[i] == '-':
                                c = c + '-'
                            else:
                                c = c + word_[i]
                        word_ = c
                        guess += 1
                    else:
                        await message.channel.send("Oh, no! You didn't guess the letter: {}!".format(ans.content))
                        lifes -= 1

                if guess == 4:
                    await message.channel.send("Congrats! You won! The word was: {}".format(word))
                    return
                elif lifes < 0:
                    await message.channel.send("Oh, no! You lost! The word was: {}".format(word))
                    return

            elif lvl.content == 'hard':
                await message.channel.send("You've picked hard level!")
                words = ['designer', 'audience',
                    'children', 'daughter', 'humanity']
                word = random.choice(words)
                word_ = '--------'
                guess = 0

                lifes = 10

                while(lifes >= 0 and guess != 8):
                    await message.channel.send("Word: {}".format(word_))
                    await message.channel.send("Guess letter! Your lifes: {}".format(lifes))

                    try:
                        ans = await self.wait_for('message', check=is_correct_letter, timeout=20.0)
                    except asyncio.TimeoutError:
                        return await message.channel.send('Sorry, time for the answer has ended!')

                    if ans.content in word:
                        await message.channel.send("Goodjob! you guessed letter: {}!".format(ans.content))
                        c = ''
                        for i in range(len(word_)):
                            if i == word.index(ans.content):
                                c = c + ans.content
                            elif word_[i] == '-':
                                c = c + '-'
                            else:
                                c = c + word_[i]
                        word_ = c
                        guess += 1
                    else:
                        await message.channel.send("Oh, no! You didn't guess the letter: {}!".format(ans.content))
                        lifes -= 1

                if guess == 8:
                    await message.channel.send("Congrats! You won! The word was: {}".format(word))
                    return
                elif lifes < 0:
                    await message.channel.send("Oh, no! You lost! The word was: {}".format(word))
                    return

        if message.content.startswith('$rps'):

            def is_correct_rps(m):
                return m.author == message.author and (m.content == 'rock' or m.content =='paper' or m.content == 'scissors')
            
            def is_correct_ys(m):
                return m.author == message.author and (m.content == 'yes'or m.content =='no')

            await message.channel.send("Let's play rock, paper, scissors!")
            while(True):
                await message.channel.send("Type rock / paper / scissors!")
                try:
                    ans = await self.wait_for('message', check=is_correct_rps, timeout=20.0)
                except asyncio.TimeoutError:
                    return await message.channel.send('Sorry, time for the answer has ended!')

                word = random.choice(['rock', 'paper', 'scissors'])

                await message.channel.send("1...")
                time.sleep(1)
                await message.channel.send("2...")
                time.sleep(1)
                await message.channel.send("3...")
                time.sleep(1)
                await message.channel.send("I chosen {}".format(word))

                if ans.content == word:
                    await message.channel.send("We have chosen the same! Let's try one more time!")
                else:
                    if ans.content == 'rock':
                        if word == 'paper':
                            await message.channel.send("I've won!!!")
                        elif word == 'scissors':
                            await message.channel.send("Congrats! You won!")
                    elif ans.content == 'paper':
                        if word == 'rock':
                            await message.channel.send("Congrats! You won!")
                        elif word == 'scissors':
                            await message.channel.send("I've won!!!")
                    elif ans.content == 'scissors':
                        if word == 'paper':
                            await message.channel.send("Congrats! You won!")
                        elif word == 'rock':
                            await message.channel.send("I've won!!!")
                    await message.channel.send("Do you want rematch? (yes / no)")
                    try:
                        ans2 = await self.wait_for('message', check=is_correct_ys, timeout=20.0)
                    except asyncio.TimeoutError:
                        return await message.channel.send('Sorry, time for the answer has ended!')
                    if ans2.content == 'no':
                        return
        if message.content.startswith('$dice'):
            await message.channel.send("Let's play guess the dice")
            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            def is_correct_ys(m):
                return m.author == message.author and (m.content == 'yes'or m.content =='no')

            while(True):
                await message.channel.send('Guess a number between 1 and 6 (the dice roll)')
                answer = random.randint(1, 6)

                try:
                    ans = await self.wait_for('message', check=is_correct, timeout=20)
                except asyncio.TimeoutError:
                    return await message.channel.send('Sorry, time for the answer has ended!')

                if int(ans.content) == answer:
                    await message.channel.send("Congrats! You won!")
                else:
                    await message.channel.send("Oh, no! You lost! The dice roll value was: {}".format(answer))
                await message.channel.send("Do you want to try again? (yes / no)")
                try:
                    ans2 = await self.wait_for('message', check=is_correct_ys, timeout=20.0)
                except asyncio.TimeoutError:
                    return await message.channel.send('Sorry, time for the answer has ended!')
                if ans2.content == 'no':
                    return
                




if __name__ == '__main__':
    client = DiscordBotClient()
    client.run(DISCORD_BOT_TOKEN)
