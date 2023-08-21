from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
import json
import puz
import tempfile
from . import forms
from .extractpuzzle import extract_grid,get_text
from .Inference import solvePuzzle

# from .extractpuzzle1 import extract_grid,get_tex
# Create your views here.

def solve(request):
    context = { }
    if ( request.method == "GET"):
        return render(request,"Solver/solver.html")
    
    if( request.method == "POST"):
        # clearing out the session
        request.session.clear()

        crossword_file = request.FILES['crossword_file']

        if crossword_file:
            # Image uploaded
            if crossword_file.content_type.startswith('image'):

                # Save the image file or perform any necessary processing
                # Get the image from the request
                image = request.FILES.get('crossword_file')

                # File was not received in the request
                if image is None:
                    return redirect('/solver')

                # Read the image using OpenCV
                img_array = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

                # trying to extract grid
                try:
                    grid_data = extract_grid(img_array)

                    print(grid_data['across_nums'])
                    print(grid_data['down_nums'])

                    rows = []
                    no_of_rows = grid_data['size']['rows']
                    no_of_cols = grid_data['size']['cols']

                    for i in range(no_of_rows):
                        temp = []
                        for j in range(no_of_cols):
                            temp.append((grid_data['gridnums'][i * no_of_cols + j], grid_data['grid'][i * no_of_cols + j],0)) # this might produce errors in case the size mismatch occurs
                        rows.append(temp)
                    
                    # just initializing empty ones
                    across_clues_dict = {}
                    down_clues_dict = {}

                    for i in grid_data['across_nums']:
                        across_clues_dict[i] = ''
                    for i in grid_data['down_nums']:
                        down_clues_dict[i] = ''

                    request.session['across_clues_dict'] =  across_clues_dict
                    request.session['down_clues_dict'] =  down_clues_dict

                    request.session['grid_extraction_failed'] = False
                    request.session['grid-rows'] = rows
                except Exception as e:
                    request.session['grid_extraction_failed'] = True
                    print("Grid Extraction thing failed:", e)

                # trying to extract clues
                try:
                    across_clues_dict = request.session.get('across_clues_dict')
                    down_clues_dict = request.session.get('down_clues_dict')

                    across, down = get_text(img_array)
                    request.session['clue_extraction_failed'] = False

                    print(across,down)

                    for key,value in across.items():
                        across_clues_dict[int(key)] = value
                    for key,value in down.items():
                        down_clues_dict[int(key)] = value

                    print(down)
                    across_clues = [(key,value.strip(".").strip(" "))for key, value in across_clues_dict.items()]
                    down_clues = [(key,value.strip(".").strip(" ")) for key, value in down_clues_dict.items()]

                    request.session['across_clues'] = across_clues
                    request.session['down_clues'] = down_clues
                except Exception as e:
                    request.session['clue_extraction_failed'] = True
                    print("Clue Extraction thing failed:", e)

                return redirect('Verify')


            # Json File Uploaded
            elif crossword_file.content_type == 'application/json':

                json_file = request.FILES.get("crossword_file")
                if json_file is None:
                    return redirect('/solver')
                grid_data = json.loads(json_file.read())

                request.session['json'] = grid_data

                # extracting grid rows
                rows = []
                no_of_rows = grid_data['size']['rows']
                no_of_cols = grid_data['size']['cols']

                for i in range(no_of_rows):
                    temp = []
                    for j in range(no_of_cols):
                        temp.append((grid_data['gridnums'][i * no_of_cols + j], grid_data['grid'][i * no_of_cols + j],0))
                    rows.append(temp)
                
                def separate_num_clues(clue):
                    arr = clue.split(".")
                    return (arr[0],"".join(arr[1:]))
                
                across_clues_num = [separate_num_clues(i) for i in grid_data['clues']['across']]
                down_clues_num = [separate_num_clues(i) for i in grid_data['clues']['down']]
                
                # updating the session
                request.session['grid_extraction_failed'] = False
                request.session['grid-rows'] = rows
                request.session['across_clues'] = across_clues_num
                request.session['down_clues'] = down_clues_num

                return redirect('Verify')
                 
            # Puz file Uploaded
            elif crossword_file.content_type == 'application/octet-stream':
                
                puz_file = request.FILES.get("crossword_file")
                if puz_file is None:
                    return redirect('/solver')
                
                # Create a temporary file because puz.read takes file_name as an arguement
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(puz_file.read())
                p = puz.read(temp_file.name)    
                numbering = p.clue_numbering()

                grid = []
                gridnum = []
                for row_idx in range(p.height):
                    cell = row_idx * p.width
                    row_solution = p.solution[cell:cell + p.width]
                    for col_index, item in enumerate(row_solution):
                        if p.solution[cell + col_index: cell + col_index + 1] == '.':
                            grid.append(".")
                            gridnum.append(0)
                        else:
                            grid.append(row_solution[col_index: col_index + 1])
                            gridnum.append(0)
                            
                across_clues = []
                for clue in numbering.across:
                    answer = str(clue['num']) + ". " + clue['clue']
                    across_clues.append(answer)
                    gridnum[int(clue['cell'])] = clue['num']

                down_clues = []
                for clue in numbering.down:
                    answer = str(clue['num']) + ". " + clue['clue']
                    down_clues.append(answer)
                    gridnum[int(clue['cell'])] = clue['num']

                # final JSON format
                grid_data = {'size': { 'rows': p.height, 'cols': p.width}, 'clues': {'across': across_clues, 'down': down_clues}, 'grid': grid,'gridnums':gridnum}
                
                # extracting grid rows
                rows = []
                no_of_rows = grid_data['size']['rows']
                no_of_cols = grid_data['size']['cols']

                for i in range(no_of_rows):
                    temp = []
                    for j in range(no_of_cols):
                        temp.append((grid_data['gridnums'][i * no_of_cols + j], grid_data['grid'][i * no_of_cols + j]))
                    rows.append(temp)
                
                # separating to [(num,clues)] format
                def separate_num_clues(clue):
                    arr = clue.split(".")
                    return (arr[0],"".join(arr[1:]))
                
                across_clues_num = [separate_num_clues(i) for i in grid_data['clues']['across']]
                down_clues_num = [separate_num_clues(i) for i in grid_data['clues']['down']]
                
                # updating the session
                request.session['grid_extraction_failed'] = False
                request.session['grid-rows'] = rows
                request.session['across_clues'] = across_clues_num
                request.session['down_clues'] = down_clues_num

                return redirect('Verify')
            else:
                return HttpResponse('Invalid file format.')
                   
    return render(request,"Solver/solver.html",context=context)

@csrf_exempt
def solve1(request):
    context = {}
    if( request.method == "POST"):
        received_data = request.body.decode('utf-8')  # Decode the byte data to a string
        print("Generating Solutions")
        # Log the received data for debugging
        solution,evaluations = solvePuzzle(request.session.get("json"))
        # printing solution
        print(solution)
        print(evaluations)

        request.session['solution'] = solution
        request.session['evalutions'] = evaluations

        # Return the received data in the response
        return redirect("Solution")
    
def showSolution(request):
    grid_rows = request.session.get("grid-rows")
    across_clues = request.session.get("across_clues")
    down_clues = request.session.get("down_clues")
    solutions = request.session.get("solution")
    evaluations = request.session.get('evalutions')


    context = {}
    for i in range(0,len(solutions)):
        for j in range(0,len(grid_rows[i])):
            grid_rows[i][j][2] = solutions[i][j] if solutions[i][j] != '' else " "


    context['grid_rows'] = grid_rows # Array of arrays 1st array element contains cell data for 1st and 1st columnrow as [ {grid_num},{grid-value}] format
    context['across_clues'] = across_clues
    context['down_clues'] = down_clues
    context['evalutions'] = evaluations

    return render(request,"Solver/solutions.html",context=context)



def verify(request):

    # dictionary with keys 
    # grid_rows = [(grid-num,grid-value)]
    # across_clues = ["1. hello mello"]
    # down_clues = ["1. hello wello"]
    context = {}
    
    if(request.method == "GET"):
        # Extracting grid and clues from the session
        grid_rows = request.session.get("grid-rows")
        across_clues = request.session.get("across_clues")
        down_clues = request.session.get("down_clues")

        # if clue extraction failed then don't show across and down clues
        if(request.session.get("clue_extraction_failed")):
            across_clues = [(1,""),(16,""),(17,""),(18,""),(19,""),(20,""),(21,""),(22,""),(23,""),(24,""),(25,""),(26,""),(27,""),(28,""),(29,"")]
            down_clues = [(1,""),(2,""),(3,""),(4,""),(5,""),(6,""),(7,""),(8,""),(9,""),(10,""),(11,""),(12,""),(13,""),(14,""),(15,"")]
            
        # if grid extraction fails then show a 15 * 15 grid
        if(request.session.get("grid_extraction_failed")):
            nums = [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],  # default grid to display
                    [16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [19,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [22,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [26,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [27,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    [29,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
                    ]
            
            rows = []
            for i in range(15):
                temp = []
                for j in range(15):
                    temp.append((nums[i][j]," "))
                rows.append(temp)
            grid_rows = rows

        print(grid_rows)
        context['grid_rows'] = grid_rows # Array of arrays 1st array element contains cell data for 1st and 1st columnrow as [ {grid_num},{grid-value}] format
        context['across_clues'] = across_clues
        context['down_clues'] = down_clues
        context['solutions'] = 0

        return render(request,"Solver/verify.html",context=context)
