from django.shortcuts import render,HttpResponse,redirect
import cv2
import numpy as np
from . import forms
from .extractpuzzle import extract_grid
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
            print(crossword_file.content_type)
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
                try: 
                    grid_data = extract_grid(img_array)
                except Exception as e:
                    HttpResponse(f'Error {e} has occured')
                else:
                    print(grid_data)
                    rows = []
                    no_of_rows = grid_data['size']['rows']
                    no_of_cols =  grid_data['size']['cols']


                    for i in range(no_of_rows):
                        temp = []
                        for j in range(no_of_cols):
                            # {grid-nums , grid-data} basically clue_no and answer_alphabet
                            print(i," ",j)
                            temp.append((grid_data['gridnums'][i * no_of_cols + j],grid_data['grid'][i * no_of_cols + j]))
                        rows.append(temp)
                    
                    context['grid_rows'] = rows # Array of arrays 1st array element contains cell data for 1st and 1st columnrow as [ {grid_num},{grid-value}] format

                    context['across_clues'] = []
                    context['down_clues'] = []
                    # context['across_clues'] = grid_data['clues']['across']
                    # context['down_clues'] = grid_data['clues']['down']
                    return render(request,'NYTgrid/NYTgrid.html', context=context)

                

            # Json File Uploaded
            elif crossword_file.content_type == 'application/json':
                return HttpResponse('JSON file uploaded successfully.')
            # Puz file Uploaded
            elif crossword_file.content_type == 'application/octet-stream':
                return HttpResponse('PUZ file uploaded successfully.')
            else:
                return HttpResponse('Invalid file format.')
                   
    return render(request,"Solver/solver.html",context=context)
