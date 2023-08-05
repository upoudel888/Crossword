class Grid{

    constructor(){
        // buttons
        this.decreaseButton = document.querySelector(".decrease-button");
        this.increaseButton = document.querySelector(".increase-button");
        this.rotateLeftButton = document.querySelector(".rot-left-button");
        this.rotateRightButton = document.querySelector(".rot-right-button");

        // variables
        this.dimension = document.querySelectorAll(".grid-row").length;
        this.grid = []          // array of arrays
        this.grid_nums = []     // array
        this.across_nums = []   // array
        this.down_nums = []     // array

        this.acrossCluesWithNums = {} // the clue and clue number extracted from the dom
        this.downCluesWithNums = {}   // these variables do not change

        this.initialize();
    }

    initialize() {
        // DOM elements 
        this.cells = document.querySelectorAll(".grid-cell");         // they change when user makes some grid changes
        this.cellNums = document.querySelectorAll(".cell-num");
        this.grid_rows = document.querySelectorAll(".grid-row");
        this.parent = document.querySelector(".grid");
        
        this.downClues =  document.querySelectorAll(".down-clue");    // the don't
        this.acrossClues = document.querySelectorAll(".across-clue");
        this.dimensionInfo = document.querySelectorAll(".dim-info");

        // "" means white cell and "." mean black cell in this.grid
        this.grid = this.getGrid();      // uses this.cells to compute the cell number                  
        this.computeGridNum();           // computes this.grid_nums, this.across_nums and this.down_nums using this.grid
        this.getCluesWithNums();         // computes this.acrossCluesWithNums and this.downCluesWithNums
        this.addCellEventListener();     // Adds click event listener to the grid cells
        this.addButtonEventListener()

        this.assignNewClues();
    }

    reinitializeAfterUpdate(){

        this.cells = document.querySelectorAll(".grid-cell");
        this.cellNums = document.querySelectorAll(".cell-num");
        this.grid_rows = document.querySelectorAll(".grid-row")
        this.parent = document.querySelector(".grid");
        
        this.grid = this.getGrid();
        this.computeGridNum();
        this.getCluesWithNums();
        this.addCellEventListener();
        this.assignNewClues();
    }

    // get across and down clues from the dom
    getCluesWithNums(){
        for(let elem of this.acrossClues){
            this.acrossCluesWithNums[elem.firstElementChild.innerText] = elem.lastElementChild.innerText;
        }

        for(let elem of this.downClues){
            this.downCluesWithNums[elem.firstElementChild.innerText] = elem.lastElementChild.innerText;
        }
    }

    createCell(){
        // Create the main grid-cell div
        const gridCellDiv = document.createElement('div');
        gridCellDiv.classList.add('grid-cell');
      
        // Create the div for cell-num
        const cellNumDiv = document.createElement('div');
        cellNumDiv.classList.add('cell-num');
      
        // Create the div for cell-data
        const cellDataDiv = document.createElement('div');
        cellDataDiv.classList.add('cell-data');
      
        // Append cell-num and cell-data divs to the main grid-cell div
        gridCellDiv.appendChild(cellNumDiv);
        gridCellDiv.appendChild(cellDataDiv);
      
        return gridCellDiv;
    }

    createRow(rowArr){
        const gridRowDiv = document.createElement('div');
        gridRowDiv.classList.add("grid-row");

        for (let cell of rowArr){
            gridRowDiv.appendChild(this.createCell());
        }
        return gridRowDiv
    }

    increaseGrid() {
        // Add a empty cell (" ") to each existing row
        for (let i = 0; i < this.dimension; i++) {
          this.grid[i].push(" "); //updating this.grid
          this.grid_rows[i].appendChild(this.createCell()); //updating dom
        }
        // Add a new row filled with empty cell at the end
        const newRow = Array(this.dimension + 1).fill(" ");
        this.grid.push(newRow); // updating this.grid
        this.parent.appendChild(this.createRow(newRow)); // updating dom

        this.dimension++;

        this.reinitializeAfterUpdate();
        this.assignNewNumbers();
    }

    decreaseGrid() {
        if (this.dimension > 1) {
          // Remove the last row
          this.grid.pop();
          this.parent.removeChild(this.parent.lastChild);
          // Remove the last character from each remaining row
          for (let i = 0; i < this.dimension - 1; i++) {
            this.grid[i].pop();
            this.grid_rows[i].removeChild(this.grid_rows[i].lastChild);
          }
          this.dimension--;
          this.reinitializeAfterUpdate();
          this.assignNewNumbers();
        }
    }

    addButtonEventListener(){
        this.decreaseButton.addEventListener('click',()=>{
            this.decreaseGrid();
            console.log(JSON.stringify(this.grid));
        })
        
        this.increaseButton.addEventListener('click',()=>{
            this.increaseGrid();
            console.log(JSON.stringify(this.grid));
        })

    }

    eventListenerFunction(cell,index){
        // original clicked position
        let click_x = Math.floor(index / this.dimension);
        let click_y = index % this.dimension;

        // mirror position
        let click_x1 = ( this.dimension - 1  ) - click_x;
        let click_y1 = ( this.dimension - 1 ) - click_y;

        // toggling the class and updating this.grid for original position
        cell.classList.toggle("dead-cell");
        if(cell.classList.contains("dead-cell")){
            this.grid[click_x][click_y] = '.';
        }else{
            this.grid[click_x][click_y] = ' ';
        }

        // toggling the class and updating this.grid for mirror position
        if( !( click_x === click_y && click_x === Math.floor(this.dimension / 2))){
            let cell_mirror = this.cells[click_x1 * this.dimension + click_y1]
            cell_mirror.classList.toggle("dead-cell");
            if(cell_mirror.classList.contains("dead-cell")){
                this.grid[click_x1][click_y1] = '.';
            }else{
                this.grid[click_x1][click_y1] = ' ';
            }
        }

        // computing new grid nums
        this.computeGridNum();
        // updating the dom with new numbers
        this.assignNewNumbers();
        // updating the dom with new clues
        this.assignNewClues();
    }
    
    // if clicked => toogle class => upadate this.grid => update this.grid_nums => update the dom
    addCellEventListener(){
        this.cells.forEach((cell,index)=>{
            cell.addEventListener('click',()=>{this.eventListenerFunction(cell,index)});
        })
    }

    removeCellEventListener(){
        this.cells.forEach((cell,index)=>{
            cell.removeEventListener('click',()=>{this.eventListenerFunction(cell,index)});
        })
    }

    // change the UI with the updated grid numbers
    assignNewNumbers(){
        for(let idx in this.grid_nums){
            if(this.grid_nums[idx] === 0){
                this.cellNums[idx].innerHTML = " ";
            }else{
                this.cellNums[idx].innerHTML = this.grid_nums[idx];
            }
        }
    }

    // delete the previous list of across and down clues
    // change the UI with newly computed across and down grid numbers
    // also update their selectors i.e. this.acrossClues and this.downClues
    assignNewClues(){
        const acrossParent = document.querySelector(".across-clues");
        const downParent = document.querySelector(".down-clues");

        // deleting previous across and down clues
        this.acrossClues.forEach((elem)=>{
            acrossParent.removeChild(elem);
        })
        this.downClues.forEach((elem)=>{
            downParent.removeChild(elem);
        })

        // adding new across clues
        this.across_nums.forEach((elem)=>{
            const divElement = document.createElement('div');
            const clueNumElement = document.createElement('div');
            const clueTextElement = document.createElement('div');
            
            const num = elem;
            let clue = this.acrossCluesWithNums[num];
            if(clue === undefined) clue = " ";

            // adding class List
            divElement.classList.add('across-clue');
            divElement.classList.add(`across-clue-${num}`);

            clueNumElement.classList.add('clue-num');
            clueTextElement.classList.add('clue-text');
            clueTextElement.setAttribute('contenteditable', true);
            clueTextElement.textContent = clue;
            clueNumElement.textContent = num;
            
            // appending the elements
            divElement.appendChild(clueNumElement);
            divElement.appendChild(clueTextElement);
            acrossParent.appendChild(divElement);

        });

        // adding new down clues
        this.down_nums.forEach((elem)=>{
            const divElement = document.createElement('div');
            const clueNumElement = document.createElement('div');
            const clueTextElement = document.createElement('div');
            
            const num = elem;
            let clue = this.downCluesWithNums[num];
            if(clue === undefined) clue = " ";

            // adding class List
            divElement.classList.add('down-clue');
            divElement.classList.add(`down-clue-${num}`);

            clueNumElement.classList.add('clue-num');
            clueTextElement.classList.add('clue-text');
            clueTextElement.setAttribute('contenteditable', true);
            clueTextElement.textContent = clue;
            clueNumElement.textContent = num;
            
            // appending the elements
            divElement.appendChild(clueNumElement);
            divElement.appendChild(clueTextElement);
            downParent.appendChild(divElement);
        });

        // updating these variables to remove in the next condition
        this.acrossClues = document.querySelectorAll(".across-clue");
        this.downClues =  document.querySelectorAll(".down-clue");
    }

    // get's the grid from the DOM once the page is loaded
    // Returns Array of Arrays
    getGrid(){
        // the main arr
        let arr = new Array();

        // row wise array appended into the main arr
        let tempArr = new Array();
        let count = 0;
        for(let cell of this.cells){
            if(cell.classList.contains("dead-cell")){
                tempArr.push(".");
            }else{
                tempArr.push(" ");
            }
            count += 1;
            // checking if a row has been completed
            if((count % this.dimension == 0)){
                arr.push(tempArr)
                tempArr = []
            }
        }
        return arr;
    }

    // computes the grid num from using the grid colors ( it uses this.grid to see the colors )
    // returns an array
    computeGridNum() {

        this.grid_nums = [];
        this.across_nums = [];
        this.down_nums = [];
        let in_horizontal = [];
        let in_vertical = [];
        let num = 0;
    
        for (let x = 0; x < this.dimension; x++) {
            for (let y = 0; y < this.dimension; y++) {
                // If there is a black cell, then there's no need to number
                if (this.grid[x][y] === ".") {
                    this.grid_nums.push(0);
                    continue;
                }
    
                // Check if the cell is part of both horizontal and vertical cells
                let horizontal_presence = in_horizontal.some(coord => coord[0] === x && coord[1] === y);
                let vertical_presence = in_vertical.some(coord => coord[0] === x && coord[1] === y);
    
                // If present in both (1 1)
                if (horizontal_presence && vertical_presence) {
                    this.grid_nums.push(0);
                    continue;
                }
    
                // If present in one (1 0)
                if (!horizontal_presence && vertical_presence) {
                    let horizontal_length = 0;
                    let temp_horizontal_arr = [];
    
                    // Iterate in x direction until the end of the grid or until a black box is found
                    while (x + horizontal_length < this.dimension && this.grid[x + horizontal_length][y] !== '.') {
                        temp_horizontal_arr.push([x + horizontal_length, y]);
                        horizontal_length++;
                    }
    
                    // If horizontal length is greater than 1, then append the temp_horizontal_arr to in_horizontal array
                    if (horizontal_length > 1) {
                        in_horizontal.push(...temp_horizontal_arr);
                        num++;
                        this.across_nums.push(num)
                        this.grid_nums.push(num);
                        continue;
                    }
    
                    this.grid_nums.push(0);
                }
    
                // If present in one (0 1)
                if (!vertical_presence && horizontal_presence) {
                    let vertical_length = 0;
                    let temp_vertical_arr = [];
    
                    // Iterate in y direction until the end of the grid or until a black box is found
                    while (y + vertical_length < this.dimension && this.grid[x][y + vertical_length] !== '.') {
                        temp_vertical_arr.push([x, y + vertical_length]);
                        vertical_length++;
                    }
    
                    // If vertical length is greater than 1, then append the temp_vertical_arr to in_vertical array
                    if (vertical_length > 1) {
                        in_vertical.push(...temp_vertical_arr);
                        num++;
                        this.down_nums.push(num)
                        this.grid_nums.push(num);
                        continue;
                    }
    
                    this.grid_nums.push(0);
                }
    
                // If not present in both (0 0)
                if (!horizontal_presence && !vertical_presence) {
                    let horizontal_length = 0;
                    let temp_horizontal_arr = [];
                    let vertical_length = 0;
                    let temp_vertical_arr = [];
    
                    // Iterate in x direction until the end of the grid or until a black box is found
                    while (x + horizontal_length < this.dimension && this.grid[x + horizontal_length][y] !== '.') {
                        temp_horizontal_arr.push([x + horizontal_length, y]);
                        horizontal_length++;
                    }
    
                    // Iterate in y direction until the end of the grid or until a black box is found
                    while (y + vertical_length < this.dimension && this.grid[x][y + vertical_length] !== '.') {
                        temp_vertical_arr.push([x, y + vertical_length]);
                        vertical_length++;
                    }
    
                    // If both horizontal and vertical lengths are greater than 1, then update both in_horizontal and in_vertical arrays
                    if (horizontal_length > 1 && vertical_length > 1) {
                        in_horizontal.push(...temp_horizontal_arr);
                        in_vertical.push(...temp_vertical_arr);
                        num++;
                        this.across_nums.push(num);
                        this.down_nums.push(num);
                        this.grid_nums.push(num);
                    }
                    // If only vertical length is greater than 1, then update in_vertical array
                    else if (vertical_length > 1) {
                        in_vertical.push(...temp_vertical_arr);
                        num++;
                        this.down_nums.push(num);
                        this.grid_nums.push(num);
                    }
                    // If only horizontal length is greater than 1, then update in_horizontal array
                    else if (horizontal_length > 1) {
                        in_horizontal.push(...temp_horizontal_arr);
                        num++;
                        this.across_nums.push(num);
                        this.grid_nums.push(num);
                    } else {
                        this.grid_nums.push(0);
                    }
                }
            }
        }

        // I don't know why my logic is opposite XD
        let temp = this.down_nums;
        this.down_nums = JSON.parse(JSON.stringify(this.across_nums));
        this.across_nums = JSON.parse(JSON.stringify(temp));
    }

    
}

let grid = new Grid();
