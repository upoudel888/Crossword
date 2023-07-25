from django.shortcuts import render,HttpResponse,redirect
import cv2
import numpy as np
import json
import puz
import tempfile
from . import forms
from .extractpuzzle import extract_grid,get_text

# from .extractpuzzle1 import extract_grid,get_tex
# Create your views here.

def solve(request):
    context = {
        'form' : forms.UserImagesForm()
    }
    if ( request.method == "GET"):
        return render(request,"Solver/solver.html",context=context)
    
    if( request.method == "POST"):
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
                img_array = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

                try:
                    grid_data = extract_grid(img_array)

                    rows = []
                    no_of_rows = grid_data['size']['rows']
                    no_of_cols = grid_data['size']['cols']

                    for i in range(no_of_rows):
                        temp = []
                        for j in range(no_of_cols):
                            temp.append((grid_data['gridnums'][i * no_of_cols + j], grid_data['grid'][i * no_of_cols + j]))
                        rows.append(temp)
                
                    request.session['grid_extraction_failed'] = False
                    request.session['grid-rows'] = rows
                except Exception as e:
                    request.session['grid_extraction_failed'] = True
                    print("Grid Extraction thing failed:", e)

                try:
                    across, down = get_text(img_array)
                    request.session['clue_extraction_failed'] = False

                    across_clues = [str(int(key)) + "   " + value for key, value in across.items()]
                    down_clues = [str(int(key)) + "   " + value for key, value in down.items()]

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

                # extracting grid rows
                rows = []
                no_of_rows = grid_data['size']['rows']
                no_of_cols = grid_data['size']['cols']

                for i in range(no_of_rows):
                    temp = []
                    for j in range(no_of_cols):
                        temp.append((grid_data['gridnums'][i * no_of_cols + j], grid_data['grid'][i * no_of_cols + j]))
                    rows.append(temp)
                
                # updating the session
                request.session['grid_extraction_failed'] = False
                request.session['grid-rows'] = rows
                request.session['across_clues'] = grid_data['clues']['across']
                request.session['down_clues'] = grid_data['clues']['down']

                return redirect('Verify')
                 
            # Puz file Uploaded
            elif crossword_file.content_type == 'application/octet-stream':
                puz_file = request.FILES.get("crossword_file")
                if puz_file is None:
                    return redirect('/solver')
                
                # Create a temporary file
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
                
                # updating the session
                request.session['grid_extraction_failed'] = False
                request.session['grid-rows'] = rows
                request.session['across_clues'] = grid_data['clues']['across']
                request.session['down_clues'] = grid_data['clues']['down']

                return redirect('Verify')
            else:
                return HttpResponse('Invalid file format.')
                   
    return render(request,"Solver/solver.html",context=context)

def verify(request):

    context = {}
    
    if(request.method == "GET"):
        grid_rows = request.session.get("grid-rows")
        across_clues = request.session.get("across_clues")
        down_clues = request.session.get("down_clues")

        if(request.session.get("clue_extraction_failed")):
            across_clues = []
            down_clues = []
        if(request.session.get("grid_extraction_failed")):
            nums = [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
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


        context['grid_rows'] = grid_rows # Array of arrays 1st array element contains cell data for 1st and 1st columnrow as [ {grid_num},{grid-value}] format
        context['across_clues'] = across_clues
        context['down_clues'] = down_clues

        return render(request,"Solver/verify.html",context=context)
