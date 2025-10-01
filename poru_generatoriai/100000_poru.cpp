#include <iostream>
#include <fstream>
#include <string>
#include <random>
#include <vector>
using namespace std;

// Random string generatorius
string random_string(size_t length, mt19937 &rng) {
    static const string alphabet =
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    uniform_int_distribution<int> dist(0, (int)alphabet.size() - 1);
    string s;
    s.reserve(length);
    for (size_t i = 0; i < length; i++) {
        s.push_back(alphabet[dist(rng)]);
    }
    return s;
}

int main() {
    mt19937 rng(random_device{}());

    vector<int> lengths = {10, 100, 500, 1000};
    int pairs = 100000;

    ofstream fout("poros.txt"); // viską į failą
    if (!fout) {
        cerr << "Nepavyko atidaryti failo\n";
        return 1;
    }

    for (int L : lengths) {
        fout << "=== Ilgis " << L << " ===\n";
        for (int i = 0; i < pairs; i++) {
            string s1 = random_string(L, rng);
            string s2 = random_string(L, rng);
            fout << s1 << " " << s2 << "\n";
        }
        fout << "\n";
    }

    fout.close();
    cout << "Sugeneruotos poros issaugotos faile poros.txt\n";
    return 0;
}
