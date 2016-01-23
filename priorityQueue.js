function print(x){
	console.log(x);
}

function len(x){
	return x.length;
}

// Priority Queue using Binary Heap
function heapPQ(data){
	this.heap = data;
	this.track = [];                 // Keeps track of the original idices of the data -> for update and search in O(log(n)) time.
	this.addTracker = addTracker;    // Initializes track array O(n) ---- One time operation.
	this.min_heapify = min_heapify;  // O(log(n)).
	this.buildHeap = buildHeap;      // Linear -> O(n) ---- One time operation.
	this.extractMin = extractMin;    // Removes min -> O(log(n)).
	this.min  = min;                 // Gives the min w/o removing.
	this.insert = insert;            // Insert new Node to heap -> O(log(n)).
	this.update = update;            // Update a Node in heap based on original track idx (Not heap idx)-> O(log(n)).
	this.deleteNode = deleteNode;    // Delete a Node in heap based on original track idx (Not heap idx) -> O(log(n)).
	this.moveUp = moveUp;            // Move up a newly inserted OR recently updates node -> O(log(n)).
	this.lChild = lChild;
	this.rChild = rChild;
	this.getValue = getValue;
	this.getKey = getKey;
	this.swap = swap;                // Swap 2 nodes in the heap.
}

function heapNode(value, key){
	this.value = value;
	this.key = key;
	this.idx = null;
}

function parent(i){
	return Math.floor(i/2);
}

function lChild(i){
	var val = (i*2) + 1;
	if(val > len(this.heap)-1){
		return null;
	}
	return val;
}

function rChild(i){
	var val = (i*2) + 2;
	if(val > len(this.heap)-1){
		return null;
	}
	return val;
}

function getValue(i){
	return this.heap[i].value;
}

function getKey(i){
	return this.heap[i].key;
}

function swap(a, b){
	var tmp = this.heap[a];
	this.heap[a] = this.heap[b];
	this.heap[a].idx = a
	this.heap[b] = tmp; 
	this.heap[b].idx = b;
}

function min_heapify(x){
	l_c = this.lChild(x);
	r_c = this.rChild(x);

	var smallest = x;
	if (l_c != null && this.getValue(l_c) < this.getValue(smallest) ){
		smallest = l_c;
	}
	if (r_c != null && this.getValue(r_c) < this.getValue(smallest) ){
		smallest = r_c;
	}
	if (smallest != x) {
		this.swap(smallest,x);
		this.min_heapify(smallest)
	}
}

function addTracker(){
	var n = len(this.heap);
	for(var i = 0; i<n; i++){
		this.track.push(this.heap[i]);
	}
}
function buildHeap(){
	var lastIdx = len(this.heap) - 1;
	for(var i = parent(lastIdx); i >= 0; i--){
		this.min_heapify(i);
	}
}

function extractMin(){
	var firstIdx = 0;
	var lastIdx = len(this.heap) - 1;
	this.swap(firstIdx, lastIdx);
	
	var min = this.heap[lastIdx];
	this.heap.pop();
	this.min_heapify(firstIdx);
	return min;
}

function min(){
	return this.heap[0];
}

function moveUp(i){
	if(this.getValue(i) < this.getValue(parent(i))){
			this.swap(i,parent(i));
			this.moveUp(parent(i));
		}
}

function update(trackIdx, newValue){
	var heapIdx = this.track[trackIdx].idx;
	if(heapIdx < len(this.heap)){
		this.heap[heapIdx].value = newValue;
		if(newValue < this.getValue(parent(heapIdx)) ) {
			this.moveUp(heapIdx);
		}
		else{
			this.min_heapify(heapIdx)
		}
	}
}

function insert(newNode){
	this.heap.push(newNode);
	newNode.idx = len(this.heap) - 1;
	this.track.push(newNode);
	this.moveUp(len(this.heap)-1);
}

function deleteNode(trackIdx){
	var minValue = this.getValue(0);
	this.update(trackIdx, minValue - 1);
	this.extractMin();
}


//------------------
//-----Demo Run-----
//------------------

var data = [8,2,3,0,8,5,1,34,6,233,5,45,2]
var data2 = []
for(var i =0 ; i< len(data); i++){
	var t  = new heapNode(data[i], null);
	t.idx = i;
	data2.push(t);
}

var obj = new heapPQ(data2);
obj.addTracker();
obj.buildHeap();
obj.update(3,130);
print(obj.min().value);
obj.update(11,30);
print(obj.min().value);
obj.update(7,55);
print(obj.min().value);
obj.insert(new heapNode(-100, null));
print(obj.min().value);
obj.deleteNode(9);
print(obj.min().value);
obj.deleteNode(13);
print(obj.min().value);
print('------');
n = len(obj.heap); 
// Heap-Sort :D
for(var i = 0 ; i < n; i++){
	print(obj.extractMin().value);
}