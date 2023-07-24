class Grid{

    constructor(){
        // DOM elements
        this.cells = document.querySelectorAll(".grid-cell");
        this.cellNums = document.querySelectorAll(".cell-num");
        this.dimension = document.querySelectorAll(".grid-row").length;
        this.parent = document.querySelector(".grid");
        // variables
        this.grid_nums = []  // array
        this.initialize();
    }

    initialize() {
        // "" means white cell and "." mean black cell
        this.grid = this.getGrid();                         // Array of Arrays
        this.computeGridNum();         
        this.addCellEventListener();                        // Adds click event listener to the grid cells
    }

    // if clicked => toogle class => upadate this.grid => update this.grid_nums => update the dom
    addCellEventListener(){
        this.cells.forEach((cell,index)=>{
            cell.addEventListener('click',()=>{

                // toggling the class and updating this.grid
                cell.classList.toggle("dead-cell");
                if(cell.classList.contains("dead-cell")){
                    this.grid[Math.floor(index / this.dimension)][index % this.dimension] = '.'
                }else{
                    this.grid[Math.floor(index / this.dimension)][index % this.dimension] = ' '
                }
                console.log(this.grid)
                // computing new grid nums
                this.computeGridNum();
                console.log(JSON.stringify(this.grid_nums))
                // updating the dom
                this.assignNewNumbers();
            });
        })
    }

    assignNewNumbers(){
        for(let idx in this.grid_nums){
            if(this.grid_nums[idx] === 0){
                this.cellNums[idx].innerHTML = " ";
            }else{
                this.cellNums[idx].innerHTML = this.grid_nums[idx];
            }
        }
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

    // computes the grid num from using the grid colors
    // returns an array
    computeGridNum() {

        this.grid_nums = [];
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
                        this.grid_nums.push(num);
                    }
                    // If only vertical length is greater than 1, then update in_vertical array
                    else if (vertical_length > 1) {
                        in_vertical.push(...temp_vertical_arr);
                        num++;
                        this.grid_nums.push(num);
                    }
                    // If only horizontal length is greater than 1, then update in_horizontal array
                    else if (horizontal_length > 1) {
                        in_horizontal.push(...temp_horizontal_arr);
                        num++;
                        this.grid_nums.push(num);
                    } else {
                        this.grid_nums.push(0);
                    }
                }
            }
        }
    }

    
}

let grid = new Grid();
