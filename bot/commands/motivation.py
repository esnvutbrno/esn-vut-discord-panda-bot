from datetime import datetime
from random import choice, randint
from typing import Optional

from discord import Member, Role
from discord.ext.commands import Context

from .. import bot
from ..conf import PANDA_EMOJI
from ..utils import local_seed, reply_embed, MemberIncludingAuthorConverter

QUOTES = (
    "“Service to others is the rent you pay for your room here on Earth.”**  — Muhammad Ali** ",
    "“Volunteers don’t get paid, not because they’re worthless, but because they’re priceless.” ** – Sherry Anderson** ",
    "“Remember that the happiest people are not those getting more, but those giving more.” ** ― H. Jackson Brown Jr.** ",
    "“The best way to find yourself is to lose yourself in the service of others.” ** — Mahatma Gandhi** ",
    "“The smallest act of kindness is worth more than the grandest intention.”  ** – Oscar Wilde** ",
    "“If our hopes of building a better and safer world are to become more than wishful thinking, we will need the engagement of volunteers more than ever.” ** — Kofi Annan** ",
    "“As you grow older, you will discover that you have two hands — one for helping yourself, the other for helping others.” ** — Audrey Hepburn** ",
    "“Volunteers are the only human beings on the face of the earth who reflect this nation’s compassion, unselfish caring, patience, and just plain loving one another.” ** – Erma Bombeck** ",
    "“You may not have saved a lot of money in your life, but if you have saved a lot of heartaches for other folks, you are a pretty rich man.” ** – Seth Parker** ",
    "“Life’s most persistent and urgent question is, What are you doing for others?” ** — Martin Luther King, Jr.** ",
    "“Our generation has the ability and the responsibility to make our ever-more connected world a more hopeful, stable and peaceful place.” ** — Natalie Portman** ",
    "“The purpose of life is not to be happy, but to matter– to be productive, to be useful, to have it make some difference that you have lived at all.” ** – Leo Rosten** ",
    "“If you want to touch the past, touch a rock.  If you want to touch the present, touch a flower.  If you want to touch the future, touch a life.”**  – Author Unknown** ",
    "“The meaning of life is to find your gift. The purpose of life is to give it away.” ** — William Shakespeare** ",
    "“The unselfish effort to bring cheer to others will be the beginning of a happier life for ourselves.” ** — Helen Keller** ",
    "“Volunteers do not necessarily have the time; they just have the heart.” ** – Elizabeth Andrew** ",
    "“No one is more cherished in this world than someone who lightens the burden of another.” ** – Author Unknown** ",
    "“The only people with whom you should try to get even are those who have helped you.”  ** – John E. Southard** ",
    "“It’s easy to make a buck.  It’s a lot tougher to make a difference. ” ** – Tom Brokaw** ",
    "“Act as if what you do makes a difference.  It does.”  ** – William James** ",
    "“We make a living by what we get, but we make a life by what we give.” ** — Winston Churchill** ",
    "“If you become a helper of hearts, springs of wisdom will flow from your heart.” ** – Rumi** ",
    "“Volunteers are love in motion!” ** – Author Unknown** ",
    "“The broadest, and maybe the most meaningful definition of volunteering:  Doing more than you have to because you want to, in a cause you consider good. ” ** – Ivan Scheier** ",
    "“How wonderful it is that nobody need wait a single moment before starting to improve the world.”  ** –Anne Frank** ",
    "“Being good is commendable, but only when it is combined with doing good is it useful.” ** – Author Unknown** ",
    "“Help one another. There’s no time like the present, and no present like the time.” ** – James Durst** ",
    "“Unless someone like you cares a whole awful lot, nothing is going to get better. It’s not.” ** – Dr. Seuss** ",
    "“I am a little pencil in the hand of a writing God who is sending a love letter to the world.” ** – Mother Teresa** ",
    "“While earning your daily bread, be sure you share a slice with those less fortunate.” ** –Quoted in <em>P.S. I Love You</em>, compiled by H. Jackson Brown, Jr.** ",
    "“One can pay back the loan of gold, but one dies forever in debt to those who are kind.” ** – Malayan Proverb** ",
    "“At the end of the day it’s not about what you have or even what you’ve accomplished… it’s about who you’ve lifted up, who you’ve made better. It’s about what you’ve given back.” ** – Denzel Washington** ",
    "“Even if you just change one life, you’ve changed the world forever.” ** – Mike Satterfield** ",
    "“You give but little when you give of your possessions.  It is when you give of yourself that you truly give.”**  – Kahlil Gibran** ",
    "“I am only one, but I am one.  I cannot do everything, but I can do something.  And I will not let what I cannot do interfere with what I can do.” ** – Edward Everett Hale** ",
    "“Volunteering is the ultimate exercise in democracy.  You vote in elections once a year, but when you volunteer, you vote every day about the kind of community you want to live in.” ** – Author Unknown** ",
    "“Those who bring sunshine to the lives of others cannot keep it from themselves.” ** – James Matthew Barrie** ",
    "“What we have done for ourselves alone dies with us; what we have done for others and the world remains and is immortal.” ** – Albert Pike** ",
    "“It’s nice to be important, but it’s more important to be nice.”**  – Author Unknown** ",
    "“The work an unknown good man has done is like a vein of water flowing hidden underground, secretly making the ground green.” ** – Thomas Carlyle** ",
    "“Even if it’s a little thing, do something for those who have need of a man’s help– something for which you get no pay but the privilege of doing it. For, remember, you don’t live in a world all your own. Your brothers are here, too.” ** – Albert Schweitzer** ",
    "“I’ve learned that you shouldn’t go through life with a catcher’s mitt on both hands.  You need to be able to throw something back.” ** – Maya Angelou** ",
    "“Kindness, like a boomerang, always returns.” ** – Author Unknown** ",
    "“Too often we underestimate the power of a touch, a smile, a kind word, a listening ear, an honest compliment, or the smallest act of caring, all of which have the potential to turn a life around.” ** – Leo Buscaglia** ",
    "“The true meaning of life is to plant trees under whose shade you do not expect to sit.” ** –Nelson Henderson** ",
    "“Not only must we be good, but we must also be good for something.”**  – Henry David Thoreau** ",
    "“We cannot live only for ourselves. A thousand fibers connect us with our fellow men.” ** – Herman Melville** ",
    "“If you think you are too small to be effective, you have never been in bed with a mosquito.” ** – Betty Reese** ",
    "“Wherever there is a human being, there is an opportunity for a kindness.” ** – Seneca** ",
    "“Everybody can be great. Because anybody can serve. You don’t have to have a college degree to serve. You don’t have to make your subject and your verb agree to serve. You don’t have to know the second theory of thermodynamics in physics to serve. You only need a heart full of grace. A soul generated by love.” ** – Martin Luther King, Jr.**",
)


@bot.command(
    description='Send me some supportive quote!',
    brief='Do you want to motivate somebody?',
)
async def motivate(ctx: Context, who: MemberIncludingAuthorConverter = None):
    eol = '\n'
    await ctx.send(f"{f'Only for {who.mention}:{eol}' if who else ''}> {choice(QUOTES)}")


@bot.command(
    description='Tell me Panda\'s favorite member',
    brief='Who is Panda\'s favorite member?',
    usage='[<user-role-to-choose-member-from>]',
    aliases=('favourite', 'fav')
)
async def favorite(ctx: Context, role: Optional[Role] = None):
    members = role.members if role else (ctx.guild.members if ctx.guild else [])

    if not members:
        await ctx.message.add_reaction('⁉️')
        return

    now = datetime.now()
    with local_seed(hash(f'{now.day}-{now.hour}-{now.minute // 10}')):
        fav_member = choice(members)

    if role:
        await ctx.send(f"My favorite {role} member is now {fav_member.mention}. ❤️")
    else:
        await ctx.send(f"My favorite member is now {fav_member.mention}. ❤️")


@bot.command(
    description='Tell me current value of ESN spirit',
    brief='What\'s the current value of ESN spirit?',
    aliases=('esn-spirit',)
)
async def spirit(ctx: Context):
    now = datetime.now()

    with local_seed(hash(f'{now.day}-{now.hour}-{now.minute // 10}')):
        value = randint(42, 10 ** 3)

    await ctx.send(f"The current value of the **ESN spirit is {value}**️. {PANDA_EMOJI}")

@bot.command(
    description='High-five somebody to support him or her!',
    brief='Do you want to congratulate to somebody?',
    aliases=('highfive', 'high-five',)
)
async def high_five(ctx: Context, who: MemberIncludingAuthorConverter = None):
    who = who or ctx.author
    await ctx.send(f"**Highfive for **{who.mention}! 🙏")