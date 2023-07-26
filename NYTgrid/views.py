from django.shortcuts import render
import requests
import json

from django.template.defaulttags import register

@register.filter
def get_range(value):
    return range(int(value))

@register.filter
def get_grid_element(data, i, j):
    return data[i * 15 + j]
    

# Create your views here.
def welcome(request):
    return render(request,'NYTgrid/base.html')


def getGrid(request):

    headers = {
        'Referer': 'https://www.xwordinfo.com/JSON/'
    }
    # mm/dd/yyyy
    url = 'https://www.xwordinfo.com/JSON/Data.ashx?date=07/10/2023'

    response = requests.get(url, headers=headers)

    context = {}
    if response.status_code == 200:
        bytevalue = response.content
        jsonText = bytevalue.decode('utf-8').replace("'", '"')
        grid_data = json.loads(jsonText) 
        context['data'] = grid_data
    else:
        print(f"Request failed with status code {response.status_code}.")

    rows = []
    no_of_rows = grid_data['size']['rows']
    no_of_cols =  grid_data['size']['cols']

    for i in range(no_of_rows):
        temp = []
        for j in range(no_of_cols):
            # {grid-nums , grid-data} basically clue_no and answer_alphabet
            temp.append((grid_data['gridnums'][i * no_of_rows + j],grid_data['grid'][i * no_of_rows + j]))
        rows.append(temp)

                                  
    context['grid_rows'] = rows # Array of arrays 1st array element contains cell data for 1st and 1st columnrow as [ {grid_num},{grid-value}] format
    context['across_clues'] = grid_data['clues']['across']
    context['down_clues'] = grid_data['clues']['down']


    return render(request,'NYTgrid/NYTgrid.html', context=context)


data = {
    'size': { 'rows': 15, 'cols': 15 },
    'grid': [
        " "," "," "," "," "," "," "," "," "," ",".","."," "," "," ",
        " ", " "," "," "," "," "," "," "," "," ","."," "," "," "," ",
        " "," "," "," "," "," "," "," "," "," ","."," "," "," "," ",
        " "," "," "," "," "," ","."," "," "," "," "," "," "," "," "," ",
        " "," ","."," "," "," ",".",".","."," "," "," "," ",".",".",".",
        ".","."," "," "," ","."," "," "," "," "," "," "," "," "," "," "," ",".",
        " "," "," "," "," "," "," "," "," "," "," "," "," "," ","."," "," ",
        " "," "," ","."," "," "," "," "," "," "," "," "," "," "," "," "," ",
        " ","."," "," "," "," "," "," "," "," "," "," "," ","."," "," "," ",".",".",
        ".",".","."," "," "," "," ",".",".","."," "," "," ","."," "," "," "," "," "," ",
        " "," "," "," "," ","."," "," "," "," "," "," "," "," "," "," ","."," "," ",
        " "," "," "," "," "," "," "," "," "," "," "," ","."," "," "," "," "," ",
        " "," "," "," "," "," "," "," ",".","."," "," "," "," "," "," "," "," "," "," ",
    ],
    'gridnums': [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 0, 11, 12, 13, 14, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 15, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 18, 0, 0,
        0, 0, 0, 0, 19, 0, 0, 20, 0, 0, 0, 0, 21, 0, 0, 0, 22, 0, 23, 0, 0, 0, 24,
        0, 0, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 26, 27, 0, 0, 0, 0, 28, 29, 30, 31, 32,
        0, 33, 0, 34, 0, 0, 0, 0, 0, 0, 0, 35, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0, 37, 0,
        0, 0, 38, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 40, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0,
        0, 42, 0, 43, 0, 0, 0, 0, 0, 44, 0, 0, 0, 0, 0, 0, 45, 0, 0, 0, 46, 47, 48,
        49, 0, 0, 0, 0, 50, 51, 52, 0, 53, 0, 54, 0, 0, 0, 55, 0, 0, 0, 0, 56, 0, 0,
        57, 0, 0, 0, 0, 0, 0, 58, 0, 0, 0, 0, 59, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60, 0,
        0, 0, 0, 61, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ],
    'clues': {
        'across': [
        "1. &quot;Shoot!&quot;",
        "11. It&#39;s turned down at a hotel",
        "14. Living under a rock, say",
        "15. Language that Minecraft was written in",
        "16. How hors d&#39;oeuvres are served",
        "17. Squeezed (out)",
        "18. 1996 horror classic originally titled &quot;Scary Movie&quot;",
        "19. Major upsets, e.g.",
        "21. &quot;Yikes!&quot;",
        "22. Only chemical element whose name fits this answer&#39;s length",
        "24. Bell of the synth-pop duo Erasure",
        "25. Cone head?",
        "26. Die-hard enthusiasts, and then some",
        "29. Moisten, in a way",
        "33. Eco-centric college class, informally?",
        "35. At some previous point",
        "36. Produced, as digital currency",
        "37. Wild-tasting",
        "38. He&#39;s a mensch",
        "40. J. M. Barrie boatswain",
        "41. Something people trip on, informally",
        "42. Half of a classic Hanna-Barbera cartoon duo",
        "44. ___ Aarnio, interior designer who created the bubble chair",
        "45. Refuse to settle, say",
        "46. A-line line",
        "49. Early flat screen",
        "53. Capital in Lewis and Clark County",
        "55. &quot;I thought of a joke about ___, but it&#39;s too corny&quot; (groaner)",
        "56. Here, to locals",
        "58. Urge",
        "59. Chores, typically",
        "60. Word on either side of &quot;vs.&quot;",
        "61. Some sleeveless frocks",
        ],
        'down': [
        "1. Kids&#39; game cry",
        "2. Unit of measure that has a shared etymology with &quot;inch&quot;",
        "3. Striking",
        "4. Word at the center of Rhode Island&#39;s flag",
        "5. They&#39;re just above C&#39;s",
        "6. If not more",
        "7. Go green, perhaps?",
        "8. &quot;Shoot!&quot;",
        "9. Founder of the label Rhyme Syndicate Records",
        "10. See-___",
        "11. Bit of casino restaurant fare?",
        "12. &quot;Ugh, this always happens to me!&quot;",
        "13. Longtime A&W competitor",
        "15. He hosted the first &quot;Jeopardy!&quot; in the post-Trebek era",
        "20. Squat",
        "23. Policy at some bars and eating establishments",
        "26. People of Unalaska",
        "27. Start of some juicy gossip",
        "28. Ophthalmologists call it a hordeolum",
        "29. What might surround a trunk",
        "30. Having been informed",
        "31. Drive off",
        "32. Bill Clinton played one on &quot;The Arsenio Hall Show&quot; in 1992",
        "34. Namibia neighbor: Abbr.",
        "39. Downfall",
        "43. Human-shaped board game piece",
        "46. ___ journey (literary archetype)",
        "47. Parisian preposition",
        "48. Guy Fawkes Night accessories",
        "49. Many posts, informally",
        "50. Things of use to note takers?",
        "51. Miami school, casually",
        "52. John who was a pioneer in set theory",
        "54. Code components",
        "57. Cookie Monster&#39;s real name",
        ],
    }
}
