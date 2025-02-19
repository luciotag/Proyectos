#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>
#include <unordered_map>
#include <set>
#include <map>
using namespace std;

class DisjointSet {  //es la estrucutra para saber, para cada nodo a que componente conexa pertenece. Cada una de las componentes conexas esta representada por un nodo.
    vector<int> rank, parent;
public:
    DisjointSet(int n) {
        rank.resize(n + 1, 0); //cantidad de nodos que tiene una componente conexa (rank).
        parent.resize(n + 1); // parent el padre de cada nodo.
        for (int i = 0; i < n + 1; i++) { // cada nodo arranca siendo su propia componente conexa.
            parent[i] = i;
        }
    }

    int findSet(int node) { // me va a tirar el representante de la componente conexa.
        if (node == parent[node]) return node; // si el nodo es su mismo padre
        return parent[node] = findSet(parent[node]); // recursion hasta encontrar el nodo que concida con su padre.
    }

    void unionByRank(int u, int v) { // tenemos dos nodos de diferentes componentes conexas y los queremos unir, para que sean de la misma componente conexa.
        int uRep = findSet(u); // representate de u y de v y si tienen el mismo representante, que siga pq estan en la misma componente conexa.
        int vRep = findSet(v); 
        if (uRep == vRep) return;
        if (rank[uRep] < rank[vRep]) { // si el representante es mas chico, uno el que tiene menor rank(menos nodos) con el otro.
            parent[uRep] = vRep;
        } else if (rank[uRep] > rank[vRep]) {
            parent[vRep] = uRep;
        } else {
            parent[vRep] = uRep;
            rank[uRep]++;
        }
    }
};
    //disjointset: primero ver la cantidad de nodos que hay en componentes conexas y asignarle a cada nodo un padre. luego para optimizar el manejo de nodos dentro de las componentes, si dos nodos 
    // coinciden en una componente conexa van a tener el mismo parent. esto lo hago mediante findset() y union porque luego voy a usar kruskal y yo ahi voy a necesitar saber si dos nodos pertences al 
    // arbol generador, y si dos nodos pertenecen a la misma componente conexa, no los voy a añadir al agm ademas las operaciones son en logn.

void dfs(int node, int parent, unordered_map<int, vector<int>> &adj, unordered_map<int, int> &disc, unordered_map<int, int> &low, int &timer, set<pair<int, int>> &bridges) {
    disc[node] = low[node] = ++timer; // dfs para ver si hay puentes, porque si los hay la arista va a ser de tipo "any", si es puente va a estar en todos los arboles.

    for (auto neighbor : adj[node]) { //recorremos todos los vecinos de node, adj es un unorder_map que es un diccionario mas rapido de acceder.
        if (neighbor == parent) continue; // cambiar de nodo si se llega al padre de vuelta
        if (disc.find(neighbor) == disc.end()) { //comprueba si el vecino no fue visitado
            dfs(neighbor, node, adj, disc, low, timer, bridges); //hago dfs en ese vecino, marcandolo como un nodo que esta siendo visitado desde node.
            low[node] = min(low[node], low[neighbor]); // compara el tiempo de descubrimiento entre node y neighbor, Esto permite propagar hacia arriba el tiempo más bajo alcanzable desde los nodos descendientes de node.
            if (low[neighbor] > disc[node]) { //Esta condición determina si la arista (node, neighbor) es un puente:
                                              //Si el valor más bajo alcanzable desde neighbor (low[neighbor]) es mayor que el tiempo de descubrimiento de node (disc[node]), significa que no hay otra forma de alcanzar neighbor excepto a través de esta arista.
                                              //En otras palabras, si eliminamos la arista (node, neighbor), neighbor y su subgrafo quedarían desconectados del resto del grafo.
                                              //Si se cumple esta condición, la arista se clasifica como puente y se añade al conjunto bridges.
                bridges.insert({min(node, neighbor), max(node, neighbor)});
            }
        } else {
            low[node] = min(low[node], disc[neighbor]); //sino significa que encontramos una back-edge 
        }
    }
}

void solve(int n, int m, vector<tuple<int, int, int, int>> &edges) { // hay que fijarse para cada arista de cada peso si aparecen en todos los agms posibles.
    DisjointSet dsu(n); 
    vector<string> result(m, "at least one"); // empezamos con todos atleastone
    sort(edges.begin(), edges.end(), [](auto &e1, auto &e2) {
        return get<2>(e1) < get<2>(e2);
    });

    int startIdx = 0;

    for (int i = 0; i <= m; ++i) { // voy pasando por todas las aristas hasta que cambien de peso, cuando cambian digo bueno desde aca, hasta donde llegue,
                                   // son todas aristas del mismo peso y voy al for de adentro. con esto empiezo a procesar los agms con todas esas aristas del mismo peso.
        if (i == m || get<2>(edges[i]) != get<2>(edges[startIdx])) {
            unordered_map<int, vector<int>> adj;
            map<pair<int, int>, int> numOfConnections;

            for (int j = startIdx; j < i; ++j) { // primero me pregutno si las dos pertenecen al mismo findset(), si es asi es que no la puedo meter nunca, porque pertenecen a la misma componenete conexa
                                                 // sino, sigo.
                int u = dsu.findSet(get<0>(edges[j]));
                int v = dsu.findSet(get<1>(edges[j]));
                if (u != v) {
                    adj[u].push_back(v); // sigo con las que no son none, voy construyendo un grafo sabiendo que si hay aristas puente es any, y sino es atleastone. pero si hago dfs en todos los nodos que quedan
                                         // como la complejidad es O(N+M) si lo hago en todas las aristas y nodos se me va la complejidad entonces lo que hago es unir las componentes conexas en "un nodo" y a partir 
                                         // de esos nodos que forman componentes conexas hago dfs para detectar que tipo de aristas son. pero ocurre que pueden haber aristas que sean puentes con las componentes conexas nuevas 
                                         // pero en realidad yo se que no son any, ya que hay algunas que forman ciclos, entonces lo que hago es crear un unorder_map para ver cuantas conexiones del mismo tipo hay entre 
                                         // nodos dentro de esas nuevas componentes conexas para que no se cuenten aristas como "any" de mas y las que no tienen numOfConnections==1, son ateleastone.
                    adj[v].push_back(u);
                    numOfConnections[{min(u, v), max(u, v)}]++; 
                } else {
                    result[get<3>(edges[j])] = "none";
                }
            }

            set<pair<int, int>> bridges;
            unordered_map<int, int> disc, low;
            int timer = 0;

            for (auto &[node, _] : adj) { 
                if (disc.find(node) == disc.end()) {
                    dfs(node, -1, adj, disc, low, timer, bridges); // busco todos los puentes
                }
            }

            for (int j = startIdx; j < i; ++j) {
                int u = dsu.findSet(get<0>(edges[j]));
                int v = dsu.findSet(get<1>(edges[j]));
                if (bridges.count({min(u, v), max(u, v)}) && numOfConnections[{min(u, v), max(u, v)}] == 1) { // si es puente y tiene unumOfConnections==1 es any sino es atelastone
                    result[get<3>(edges[j])] = "any";
                }
            }

            for (int j = startIdx; j < i; ++j) {
                dsu.unionByRank(get<0>(edges[j]), get<1>(edges[j])); //agrego todas las aristas al arbol.
            }

            startIdx = i;
        }
    }

    for (const string &res : result) {
        cout << res << endl;
    }
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<tuple<int, int, int, int>> edges;
    for (int i = 0; i < m; ++i) {
        int u, v, w;
        cin >> u >> v >> w;
        edges.emplace_back(u, v, w, i);
    }
    solve(n, m, edges);
    return 0;
}



#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>
#include <unordered_map>
#include <set>
#include <map>
using namespace std;

class DisjointSet {  // Estructura para manejar componentes conexas.
    vector<int> rank, parent;
public:
    DisjointSet(int n) {
        rank.resize(n + 1, 0); // Cantidad de nodos en una componente conexa (rank).
        parent.resize(n + 1);  // Padre de cada nodo.
        for (int i = 0; i < n + 1; i++) { // Inicialmente cada nodo es su propia componente conexa.
            parent[i] = i;
        }
    }

    int findSet(int node) { // Retorna el representante de la componente conexa.
        if (node == parent[node]) return node; // Si el nodo es su propio padre.
        return parent[node] = findSet(parent[node]); // Compresión de caminos.
    }

    void unionByRank(int u, int v) { // Une dos nodos en la misma componente conexa.
        int uRep = findSet(u); // Encuentra el representante de u.
        int vRep = findSet(v); // Encuentra el representante de v.
        if (uRep == vRep) return; // Si ya están en la misma componente conexa, no hace nada.
        if (rank[uRep] < rank[vRep]) { // Une el representante con menor rango al de mayor rango.
            parent[uRep] = vRep;
        } else if (rank[uRep] > rank[vRep]) {
            parent[vRep] = uRep;
        } else {
            parent[vRep] = uRep; // Si tienen el mismo rango, incrementa el rango del nuevo representante.
            rank[uRep]++;
        }
    }
};

// DisjointSet permite identificar si dos nodos pertenecen a la misma componente conexa,
// algo esencial para evitar ciclos al construir un AGM. Las operaciones son eficientes, con complejidad logarítmica.

void dfs(int node, int parent, unordered_map<int, vector<int>> &adj, 
         unordered_map<int, int> &disc, unordered_map<int, int> &low, 
         int &timer, set<pair<int, int>> &bridges) {
    disc[node] = low[node] = ++timer; // Inicializa tiempos de descubrimiento y low.

    for (auto neighbor : adj[node]) { // Recorre los vecinos del nodo actual.
        if (neighbor == parent) continue; // Evita volver al nodo padre.
        if (disc.find(neighbor) == disc.end()) { // Si el vecino no ha sido visitado.
            dfs(neighbor, node, adj, disc, low, timer, bridges); // Llama recursivamente al DFS.
            low[node] = min(low[node], low[neighbor]); // Actualiza el valor de low del nodo actual.
            if (low[neighbor] > disc[node]) { // Si no hay un camino alternativo hacia el nodo.
                bridges.insert({min(node, neighbor), max(node, neighbor)}); // Es un puente.
            }
        } else {
            low[node] = min(low[node], disc[neighbor]); // Actualiza low si encuentra una back edge.
        }
    }
}

// DFS detecta puentes, esenciales para clasificar las aristas como "any" (puentes) o "at least one".

void solve(int n, int m, vector<tuple<int, int, int, int>> &edges) { // Clasifica cada arista en el AGM.
    DisjointSet dsu(n); 
    vector<string> result(m, "at least one"); // Inicializa todas las aristas como "at least one".
    sort(edges.begin(), edges.end(), [](auto &e1, auto &e2) {
        return get<2>(e1) < get<2>(e2); // Ordena las aristas por peso.
    });

    int startIdx = 0;

    for (int i = 0; i <= m; ++i) { 
        if (i == m || get<2>(edges[i]) != get<2>(edges[startIdx])) { // Procesa bloques de aristas con el mismo peso.
            unordered_map<int, vector<int>> adj;
            map<pair<int, int>, int> numOfConnections;

            for (int j = startIdx; j < i; ++j) { 
                int u = dsu.findSet(get<0>(edges[j])); 
                int v = dsu.findSet(get<1>(edges[j])); 
                if (u != v) { // Si los nodos no están en la misma componente conexa.
                    adj[u].push_back(v);
                    adj[v].push_back(u);
                    numOfConnections[{min(u, v), max(u, v)}]++; 
                } else { // Si ya están conectados, la arista no puede pertenecer a ningún AGM.
                    result[get<3>(edges[j])] = "none";
                }
            }

            set<pair<int, int>> bridges;
            unordered_map<int, int> disc, low;
            int timer = 0;

            for (auto &[node, _] : adj) { 
                if (disc.find(node) == disc.end()) { 
                    dfs(node, -1, adj, disc, low, timer, bridges); // Detecta puentes.
                }
            }

            for (int j = startIdx; j < i; ++j) { 
                int u = dsu.findSet(get<0>(edges[j])); 
                int v = dsu.findSet(get<1>(edges[j])); 
                if (bridges.count({min(u, v), max(u, v)}) && 
                    numOfConnections[{min(u, v), max(u, v)}] == 1) {
                    result[get<3>(edges[j])] = "any"; // Es un puente.
                }
            }

            for (int j = startIdx; j < i; ++j) { 
                dsu.unionByRank(get<0>(edges[j]), get<1>(edges[j])); // Une los nodos del bloque actual.
            }

            startIdx = i; // Avanza al siguiente bloque de aristas.
        }
    }

    for (const string &res : result) {
        cout << res << endl; // Imprime la clasificación de cada arista.
    }
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<tuple<int, int, int, int>> edges;
    for (int i = 0; i < m; ++i) {
        int u, v, w;
        cin >> u >> v >> w;
        edges.emplace_back(u, v, w, i); // Almacena las aristas con su índice original.
    }
    solve(n, m, edges); // Resuelve el problema.
    return 0;
}

