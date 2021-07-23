# Beautiful Soup
from bs4 import BeautifulSoup, Tag

#markdown & extensions
import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension

# code highlighting
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter

# MARKDOWN CONVERTER
def convertMarkdown(data):
    return markdown.markdown(data, extensions=[FencedCodeExtension()])

# CODE HIGHLIGHTING
def getLexer(name):

    #need to split the name first because its formatted like this: language-[language]
    try:
        name = name.split("-")[1]
        return get_lexer_for_filename(("." + name))

    # for some reason the value of name is sometimes: language-py
    # and sometimes it is just py
    # this is handled here
    except IndexError:
        return get_lexer_for_filename(("." + name))
    
    # if the lexer is not specified in the markdown or cannot be found
    except:
        return get_lexer_for_filename(".txt")


def highlightCode(post):

    soup = BeautifulSoup(post, 'html.parser') # create new soup instance for html parsing

    # find all of the code tags in the content and sdve them to a list
    codeTags = soup.findAll("code")

    # highlight code contained in tags and save to separate list
    highlightedCode = []
    for code in codeTags:
        
        # incase the user forgot to specify the code block language in the markdown
        if code.has_attr("class"):
            lexer = getLexer(code["class"][0])
        else:
            lexer = getLexer("language-txt") # if no language is specified use a txt lexer

        highlightedCode.append(highlight(code.text, lexer, HtmlFormatter(linenos=False))) #TODO add multilexer support
    
    #insert formatted code into their own soup objects
    codeSoups = []
    for code in highlightedCode:
        codeSoups.append(BeautifulSoup(code, 'html.parser'))

    # clear main soup code tags for formatted code to be inserted into
    for tag in codeTags:
        tag.clear()
    
    # insert code from codeSoups into main soup code tags
    for index, tag in enumerate(soup.findAll("code")):
        tag.insert(1, codeSoups[index])
    
    #and finalyyyyy.... return soup
    return soup
