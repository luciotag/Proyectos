#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

void esquinas(int n, vector<vector<int>>& aristas, vector<int>& orden) {
    vector<vector<long long>> distancia(n, vector<long long>(n, LLONG_MAX));

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (aristas[i][j] != 0) {
                distancia[i][j] = aristas[i][j];
            }
            if (i == j) {
                distancia[i][j] = 0;
            }
        }
    }

    vector<long long> res;
    reverse(orden.begin(), orden.end());

    for (int k = 0; k < n; ++k) {
        int nodo = orden[k] - 1;

        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                distancia[i][j] = min(distancia[i][j], distancia[i][nodo] + distancia[nodo][j]);
            }
        }

        long long suma_distancias = 0;
        for (int i = 0; i <= k; ++i) {
            for (int j = 0; j <= k; ++j) {
                if (i != j) {
                    suma_distancias += distancia[orden[i] - 1][orden[j] - 1];
                }
            }
        }

        res.push_back(suma_distancias);
    }

    reverse(res.begin(), res.end());
    for (const auto& r : res) {
        cout << r << " ";
    }
    cout << endl;
}

int main() {
    int n;
    cin >> n;

    vector<vector<int>> aristas(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> aristas[i][j];
        }
    }

    vector<int> orden(n);
    for (int i = 0; i < n; ++i) {
        cin >> orden[i];
    }

    esquinas(n, aristas, orden);
    return 0;
}
