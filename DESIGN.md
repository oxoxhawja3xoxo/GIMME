## A "design document" for your project in the form of a Markdown file called DESIGN.md
## that discusses, technically, how you implemented your project and why you made the
## design decisions you did. Your design document should be at least several paragraphs
## in length. Whereas your documentation is meant to be a user’s manual, consider your
## design document your opportunity to give the staff a technical tour of your project
## underneath its hood.

THE DESIGN:

I implemented my project by scraping clean all the routes from p-set 8 and setting up
shop. I started with a vision of what I wanted my product to achieve. You can learn
about my vision and goals in my video, or on the "Our Story" page. Next, before writing
any code, I designed the GIMME logo with my users in mind. These are people who are up
on trends, (or at least want to be), and people who enjoy some element of spontenaety,
as referenced by the modern pink gift, and the fact that you never know what you're going
to get when you submit a survey (more on that later). Using a custom-spaced sans-serif
font in both the logo and body texts, users can see that GIMME is a design-first company.
Functionality is great, but considering I'm the only person who worked on this project,
and I'm definitely into aesthetics more than anything, have it be known, that much of
the time spent on this project will likely go unnoticed by many, but will be the reason
why avid GIMME users remain engaged in the product.

In terms of layout, I kept it very simple, and highlighted--in pink text--all important
links and buttons. so users know what's absolutely necessary to make GIMME work. Other
links, such as searching for archived surveys, aren't pink. That was definitely something
I thought about. I don't want anyone to be confused about what they're looking for on the
page.

THE TECHNICALS:

There are a few different technical elements that really laid the foundation for
my functionality. The first is the email mechanism. I researched how to send emails
through Python, including custom To, From, and Subject fields. I even managed to include
an EMOJI in my email To field. (You should try it out, so I don't feel like I wasted time)
In all emails, there are also links, which was also something pretty challenging
to work out, as a newbie coder. Emails are sent when you request that your friend fill out
a survey and also, when you forget your password.

The second technical aspect is conducting the survey. I mostly used strategies from pset 7 to
do this, so nothing new here... for a moment.

The third technical was creating the gift database, and figuring out how to make the
gift page spit out the gifts associated with particular survey results. This involved
some strategic designing of columns and SQL querrying. The LIKE operator was particularly
challenging to use, as it struggled to find a word LIKE my variable, because it kept
thinking my variable was a string, but somehow... I made it out on the otherside. I
digress now, but as you might imagine, a big brunt of the work involved filling a defining
this gift database, and how it would connect to survey results. The database could be
more robust, but truly, I think it is a decent prototype.

Another major technical involved looking up old surveys, and then accessing the gifts
based on their survey results. There's a disconnect between those routes, since gifts
are naturally accessed by posting survey results and connecting those results to the
gift database in real time. When a user clicks on someones old results, they aren't
actually posting any input. That was a serious challenge for me. I had to work out how
to make an invisible form from searching the name, and occasion for the gift, post it
back the data base, pull the affiliated tags, throw the tags back at the gift table,
and then finally, allow the user to shop for a friend who had already filled out the
survey. I beat my head against the wall to figure out how I was going to make this happen,
but alas, it works.

The interesting and terrible part about this project is that everyday, I think of a new
feature that could make users experience better and even drive growth or revenue for this
business. Unfortunately, I need to submit this now, so I have to stop short of a great
product, but it was a good experience. I get my social life back though!





