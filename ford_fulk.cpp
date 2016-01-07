#include <iostream>
#include <string>
using namespace std;

// Vertex do not represent vertices in the graph
// They the nodes in the Adjacency List
class Vertex{
public:	
	int value;
	char type;
	int flow;
	int capacity;
	Vertex *next;

	Vertex(){
		next = NULL;
		}

	Vertex(int value){
		this->value = value;
		next = NULL;
		}
};

class Graph{
public:
	Vertex adjList[1000];
	
	Graph(int n){
		for(int i=0; i<n; i++){
			Vertex v(i);
			adjList[i] = v;
			}
		}

	void addEdge(int x, int y, int capacity){
		Vertex* v2 = new Vertex(y);
		v2->capacity = capacity;
		v2->flow = 0;
		v2->type = 'f';

		Vertex *tmp;
		tmp = &adjList[x];
		while(tmp->next != NULL){
			tmp = tmp->next;
			}
		tmp->next = v2;

		Vertex* v1 = new Vertex(x);
		v1->capacity = capacity;
		v1->flow = capacity;
		v1->type = 'b';

		tmp = &adjList[y];
		while(tmp->next != NULL){
			tmp = tmp->next;
			}
		tmp->next = v1;
		}
};

class Qnode {
public:
	int value;
	Qnode *next;
};

class Queue {
public:
	Qnode* start;
	Qnode* end;
	
	Queue(){
		start = NULL;
		end = NULL;
		}

	void push (int val){
		Qnode* v = new Qnode();
		v->value = val;
		v->next = NULL;

		if(start == NULL){
			start = v;
			end = v;
			}
		else{
			end->next = v;
			end = end->next;
			}
		}

	int pop(){
		if(start == NULL){
			return -1;
			}
		else{
			Qnode* tmp = new Qnode();
			tmp = start;
			start = start->next;
			return tmp->value;
			}
		}
	
	void printq(){
		Qnode* tmp;
		tmp = start;
		while(tmp != NULL){
			cout << tmp->value << "-";
			tmp = tmp->next;
			}
		cout << endl;
		}

	bool empty(){
		if (start == NULL)
			return true;
		else
			return false;
		}

};

class Path{
public:
	int parent[1000];
	char edge_type[1000];

	Path(int n){
		for(int i=0 ; i<n; i++){
			parent[i] = -1;
			}
		}
};

void printG(Graph*g, int n){
	for(int i=0; i<n; i++){
		cout << g->adjList[i].value << " --> ";
		Vertex *tmp;
		tmp = &g->adjList[i];
		while(tmp->next != NULL){
			cout << "( Val : " << tmp->next->value<<" , Flow : "<<tmp->next->flow<<", Capacity : "<<tmp->next->capacity<<", Type : "<<tmp->next->type<<" )";
			tmp = tmp->next;
			}
		cout << endl;
		}
	}

bool hasCapacity(Vertex* v){
	if ( (v->capacity - v->flow) > 0 ){
		return true;
		}
	return false;
	}

Path* bfs(Graph* g, int n, int start, int end){
	int visited[n];//initialize too zero
	for (int i=0; i<n; i++){
		visited[i] = 0;
		}
	
	Path *path = new Path(n);
	
	Queue q;
	
	Vertex* x = new Vertex();
	x = &g->adjList[start];
	// cout << "QUEue"<<endl;
	// 	q.printq();
	q.push(x->value);
	visited[x->value] = 1;

	while(!q.empty()){
		// cout << "QUEue"<<endl;
		// q.printq();
		int tmp = q.pop();
		// cout<<"-----------------"<< tmp <<"-----------------"<<endl;
		// printG(g,n);
		// cout<<"----------------------------------"<<endl;
		Vertex* itr = new Vertex();
		itr = &g->adjList[tmp];

		while(itr->next != NULL){
			itr = itr->next;
			// cout<<itr->value<<" - Capacity - "<< hasCapacity(itr) << endl;
			if ( visited[itr->value] == 0 && hasCapacity(itr) ){
				q.push(itr->value);
				visited[itr->value] = 1;
				path->parent[itr->value] = tmp;
				path->edge_type[itr->value] = itr->type;//type of end
				}
			}
		}
	return path;
	}


bool pathExists(Path* path, int end){
	if (path->parent[end] == -1){
		return false;
		}
	else{
		return true;
		}
	}

int bottleneck(Graph* g, Path* path, int start, int end){
	int vertex = end;
	int parent;
	int bottleneck_capacity = 999999;//uperbound
	while(vertex != start){
		parent = path->parent[vertex];

		Vertex *tmp = new Vertex();
		tmp = &g->adjList[parent];

		int min;
		while(tmp->next != NULL){
			tmp = tmp->next;
			if( tmp->value == vertex && tmp->type == path->edge_type[vertex] ){
					min = tmp->capacity - tmp->flow;
				break;
				}
			}

		if ( min<bottleneck_capacity ){
			bottleneck_capacity = min;
			}
		vertex = parent;
		}
	return bottleneck_capacity;
	}

void balance(Graph* g,int bottleneck_capacity,int from,int to,char type){
	Vertex *tmp = new Vertex();
	tmp = &g->adjList[from];

	while(tmp->next != NULL){
		tmp = tmp->next;
		if( tmp->value == to && tmp->type == type ){	
			tmp->flow -= bottleneck_capacity;
			}
		}
	}

void pushFlow(Graph* g, Path* path, int start, int end, int bottleneck_capacity){
	int vertex = end;
	int parent;
	while(vertex != start){
		parent = path->parent[vertex];

		Vertex *tmp = new Vertex();
		tmp = &g->adjList[parent];

		while(tmp->next != NULL){
			tmp = tmp->next;
			if( tmp->value == vertex && tmp->type == path->edge_type[vertex] ){
				if (tmp->type =='b'){
					tmp->flow += bottleneck_capacity;
					balance(g, bottleneck_capacity, vertex, parent, 'f');
					}
				if (tmp->type == 'f'){
					tmp->flow += bottleneck_capacity;
					balance(g, bottleneck_capacity, vertex, parent, 'b');
					}
				break;
				}
			}
		vertex = parent;
		}
	}	


int fordFulk(Graph* g, int n, int start, int end){
	Path *path = new Path(n);
	path = bfs(g,n,start,end);
	
	int bottleneck_capacity;
	int count = 0;
	// cout << "Paths Exist : "<<pathExists(path, end)<<endl;
	// cout << "================================="<<endl;
	// for(int i=0; i<n; i++){
	// 	cout << i << "Index -- ";
	// 	cout << path->parent[i]<<" -- Type --";
	// 	cout << path->edge_type[i]<< endl;
	// }
	// cout << "================================="<<endl;
	// cout<<"Count"<<count<<endl;
	while( pathExists(path, end) ){
		bottleneck_capacity = bottleneck(g, path, start, end);
		pushFlow(g, path, start, end, bottleneck_capacity);
		// count++;
		// cout << "Paths Exist : "<<pathExists(path, end)<<endl;
		// cout<<"Count"<<count<<endl;
		// cout << "================================="<<endl;
		// 	for(int i=0;i<n;i++){
		// 	cout << i << "Index -- ";
		// 	cout << path->parent[i]<<" -- Type --";
		// 	cout << path->edge_type[i]<< endl;
		// }
		// cout << "================================="<<endl;
		path = bfs(g,n,start,end);
		}
	// cout << "Paths Exist : "<<pathExists(path, end)<<endl;
	// cout<<"Count"<<count<<endl;

	// for(int i=0;i<n;i++){
	// 	cout << i << "Index -- ";
	// 	cout << path->parent[i]<<" -- Type --";
	// 	cout << path->edge_type[i]<< endl;
	// }

	// cout << "after ffs"<<endl;
	// printG(g,n);
	//chk path exists
	//find bottleneck
	//push bottleneck
	}

void minCut_bfs(Graph* g, int n, int start){
	
	int visited[n];//initialize too zero
	for (int i=0; i<n; i++ ){
		visited[i] = 0;
		}

	Queue q;
	
	Vertex* x = new Vertex();
	x = &g->adjList[start];

	q.push(x->value);
	visited[x->value] = 1;
	while( !q.empty() ){
		int tmp = q.pop();

		Vertex* itr = new Vertex();
		itr = &g->adjList[tmp];

		while(itr->next != NULL) {
			itr = itr->next;
			if (visited[itr->value]==0){
				if (hasCapacity(itr)){
					q.push(itr->value);
					visited[itr->value] = 1;
					}
				else{
					cout<< tmp << " <---> " << itr->value <<endl;
				 	}
				}
			}
		}
	}

int maxFlowValue(Graph* g, int n, int start){
	Vertex* itr = new Vertex();
	itr = &g->adjList[start];	
	int maxFlowValue = 0;
	while(itr->next != NULL) {
			itr = itr->next;
			maxFlowValue += itr->flow;
		}
	return maxFlowValue;
	}


int main(){
	cout<<endl;
	int n, start, end;
	cout << "Enter No. of Vertices in the Graph : ";
	cin >> n;
	cout << "Enter start/source index : ";
	cin >> start;
	cout << "Enter end/sink index : ";
	cin >> end;

	Graph* g = new Graph(n);
	
	// g->addEdge(0,1,20);
	// g->addEdge(0,2,10);
	// g->addEdge(1,2,30);
	// g->addEdge(1,3,10);
	// g->addEdge(2,3,20);
	
	g->addEdge(0,1,2);
	g->addEdge(0,2,3);
	g->addEdge(0,3,6);
	g->addEdge(1,3,4);
	g->addEdge(1,5,1);
	g->addEdge(2,3,2);
	g->addEdge(2,4,6);
	g->addEdge(3,5,2);
	g->addEdge(3,6,1);
	g->addEdge(4,3,4);
	g->addEdge(4,6,7);
	g->addEdge(5,6,8);

	
	// for(int i=0; i<n; i++){
	// 	cout << g->adjList[i].value << endl;
	// 	Vertex *tmp;
	// 	tmp = &g->adjList[i];
	// 	while(tmp->next!=NULL){
	// 		cout<<tmp->next->value<<"--";
	// 		tmp = tmp->next;
			
	// 	}cout<<endl;
	// }
	fordFulk(g, n, start, end);

	cout << endl << "++++++++++++++++++++++++++++++"<<endl<<endl;

	cout << "The Final flow graph is [ As Adjacency List ] :" << endl<<endl;
	printG(g,n);

	cout << endl << "++++++++++++++++++++++++++++++"<<endl<<endl;

	cout << "Value of max-flow is : " << maxFlowValue(g, n, start) << endl;
	
	cout << endl << "++++++++++++++++++++++++++++++"<<endl<<endl;
	
	cout << "The min-cut is : " << endl << endl;
	minCut_bfs(g, n, start);
	
	cout << endl << "++++++++++++++++++++++++++++++"<<endl<<endl;

	// Path *r = bfs(g,n,0,3);
	// for(int i=0;i<n;i++){
	// 	cout << i << "Index -- ";
	// 	cout << r->parent[i]<<" -- Type --";
	// 	cout << r->edge_type[i]<< endl;
	// }
	// Queue q;
	// Vertex* x = new Vertex(5);
	// q.push(x);
	// Vertex* y = new Vertex(7);
	// q.push(y);
	// Vertex* z = new Vertex(6);
	// q.push(z);
	// Vertex* w = new Vertex(6);
	// q.push(w);
	// cout << "pop" << q.pop()->value << endl;
	// cout << "pop" << q.pop()->value << endl;
	// cout << "pop" << q.pop()->value << endl;
	return 0;
};
