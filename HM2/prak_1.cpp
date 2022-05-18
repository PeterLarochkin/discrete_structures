#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <set>
#include <fstream>

#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

struct Var
{
    bool sign;
    std::string name;
    bool value;
    int number;

    Var(bool _sign, const std::string &_name) :
        sign(_sign), name(_name), value(false), number(0) {}

    Var(const Var &_a) :
        sign(_a.sign), name(_a.name), value(_a.value), number(_a.number) {}
   
    bool operator<(const Var &a) const {
        return abs(number) < abs(a.number);
    }
};

struct Truth_Table
{
    std::vector<std::vector<bool>> Table_Lines;
    int n;
    long long int exp2n;

    static long long int exp2(int n) {
        long long int result = 1;
        for (int i = 0; i < n; i++) {
            result *= 2;
        }
        return result;
    }

    Truth_Table(long long int _n) {
        n = _n;
        exp2n = exp2(n);
        std::vector<bool> x(n);
        std::vector<bool> last(n);

        for (int i = 0; i < n; i++) {
            x[i] = false;
            last[i] = true;
        }
       
        Table_Lines.push_back(x);

        while (x != last) {
            int p = n-1;

            while (x[p] >= true) {
                p--; 
            }

            x[p] = true;

            for (int i = p + 1; i < n; i++) {
                x[i] = false;
            }

            Table_Lines.push_back(x);
        }
    }

    void print() {
        for (auto line : Table_Lines) {
            for (bool i : line) {
                std::cout << int(i);
            }
            std::cout << std::endl;
        }
    }

    std::string to_string(long long int line) {
        std::string str;

        for (bool i : Table_Lines[line]) {
            str += std::to_string(int(i)); 
        }

        return str;
    }
};

typedef std::string Vertex;
typedef std::pair<Vertex, Vertex> Edge;

struct Circuit 
{
    std::vector<Vertex> V;
    std::set<Edge> E;

    Circuit() :
        V(), E() {}

    void set_vertexes(int n, int N, std::set<Var> &vs) {
        std::set<Var>::iterator it = vs.begin();

        for (int i = 0; i < n; i++) {
            V.push_back("x_" + std::to_string(i));
        } 

        for (int i = n; i < n + N; i++) {
            Var v1 = *it; it++; 
            Var v2 = *it; it++;
            Var v3 = *it; it++;
            Var v4 = *it; it++;

            if (v1.name == std::string("t_" + std::to_string(i) + "_0_0") && v1.value == 0 &&
                v2.name == std::string("t_" + std::to_string(i) + "_0_1") && v2.value == 1 &&
                v3.name == std::string("t_" + std::to_string(i) + "_1_1") && v3.value == 0 &&
                v4.name == std::string("t_" + std::to_string(i) + "_1_0") && v4.value == 1) {
                
                V.push_back("+_" + std::to_string(i));
            }
            else if (v1.value == 1 && v2.value == 1 && v3.value == 1 && v4.value == 1) {
                V.push_back("1_" + std::to_string(i));
            }
            else {
                V.push_back("&_" + std::to_string(i));
            }
        }
    }

    void print_vertexes(std::ofstream &o) {
        for (long unsigned int i = 0; i < V.size(); i++) {
            o << V[i] << "_" << std::to_string(i) << std::endl;
        }
    }

    void set_edges(int n, int N, std::set<Var> &vs) {
        for (auto v : vs) {
            for (int i = 0; i < n + N; i++) {
                for (int j = 0; j < n + N; j++) {
                    if (((v.name == std::string("c_" + std::to_string(i) + "_0_" + std::to_string(j))) ||
                         (v.name == std::string("c_" + std::to_string(i) + "_1_" + std::to_string(j)))) && (v.value == 1)) {
                        E.insert(std::pair(V[j], V[i]));     
                    }
                }
            }
        }            
    } 

    void print_edges(std::ofstream &o) {
        for (auto e : E) {
            o << "  \"" << e.first << "\" -> \"" << e.second << "\";" << std::endl;
        }
    } 
     
};

typedef std::vector<Var> Clause;
typedef std::vector<Clause> CNF;

typedef std::unordered_map<std::vector<bool>, bool> Boolean_function;

void print_clause(const Clause &cls) {
    std::cout << "(";

    for (long unsigned int i = 0; i < cls.size() - 1; i++) {
        std::string tilda;
        if (!cls[i].sign) tilda += "~";
        std::cout << tilda + cls[i].name << " v ";
    }

    std::string tilda;
    if (!cls[cls.size() - 1].sign) tilda += "~";

    std::cout << tilda + cls[cls.size() - 1].name << ")" << std::endl;
}

void print_cnf(const CNF &cnf) {
    for (Clause cls : cnf) {
        print_clause(cls);
    }
}

int main(int argc, const char **argv) {
    int n;
    int N;

    std::cin >> n;
    std::cin >> N;

    Truth_Table ttn(n);
//    ttn.print();

    Boolean_function f;
    
    for (long long int i = 0; i < ttn.exp2n; i++) {
        int name;
        std::cin >> name;

        f[ttn.Table_Lines[i]] = bool(name);
    } 
    
    CNF cnf;  

    // 1
    for (int i = n; i < n + N; ++i) {
        Clause clause1, clause2, clause3, clause4, clause5, clause6;

        clause1.push_back(Var(false, std::string("t_" + std::to_string(i) + "_0_0")));
        clause1.push_back(Var(true, std::string("t_" + std::to_string(i) + "_0_1")));

        clause2.push_back(Var(false, std::string("t_" + std::to_string(i) + "_0_0")));
        clause2.push_back(Var(true, std::string("t_" + std::to_string(i) + "_1_1")));

        clause3.push_back(Var(false, std::string("t_" + std::to_string(i) + "_0_1")));
        clause3.push_back(Var(true, std::string("t_" + std::to_string(i) + "_1_0")));

        clause4.push_back(Var(true, std::string("t_" + std::to_string(i) + "_0_1")));
        clause4.push_back(Var(true, std::string("t_" + std::to_string(i) + "_1_1")));

        clause5.push_back(Var(true, std::string("t_" + std::to_string(i) + "_0_1")));
        clause5.push_back(Var(false, std::string("t_" + std::to_string(i) + "_1_0")));

        clause6.push_back(Var(true, std::string("t_" + std::to_string(i) + "_0_0")));
        clause6.push_back(Var(false, std::string("t_" + std::to_string(i) + "_0_1")));
        clause6.push_back(Var(false, std::string("t_" + std::to_string(i) + "_1_1")));

        cnf.push_back(clause1);
        cnf.push_back(clause2);
        cnf.push_back(clause3);
        cnf.push_back(clause4);
        cnf.push_back(clause5);
        cnf.push_back(clause6);
    }
   
    // 2 
    /*
    for (int i = n; i < n + N; i++) {
        for (int k = 0; k < 2; k++) {
            for (int j1 = 0; j1 < n + N; j1++) {
                for (int j2 = 0; j2 < n + N; j2++) {
                    if (j1 < j2) {
                        Clause clause1;

                        clause1.push_back(Var(false, std::string("c_" + std::to_string(i) + "_"
                                                                   + std::to_string(k) + "_"
                                                                   + std::to_string(j1))));
                        clause1.push_back(Var(false, std::string("c_" + std::to_string(i) + "_"
                                                                   + std::to_string(k) + "_"
                                                                   + std::to_string(j2))));

                        cnf.push_back(clause1);
                    }
                }
            }
            
            Clause clause2;
            
            for (int j = 0; j < n + N; j++) {
                clause2.push_back(Var(true, std::string("c_" + std::to_string(i) + "_"
                                                             + std::to_string(k) + "_"
                                                             + std::to_string(j))));
            }

            Clause clause3;

            for (int j = 0; j < n + N; j++) {
                if (i == j) {
                    clause3.push_back(Var(false, std::string("c_" + std::to_string(i) + "_"
                                                                  + std::to_string(k) + "_"
                                                                  + std::to_string(j))));
                    cnf.push_back(clause3);
                }
            }

            cnf.push_back(clause2);
        }
    }
    */

    for (int i = n; i < n + N; i++) {
        for (int k = 0; k < 2; k++) {
            Clause clause;
            for (int j = 0; j < i; j++) {
                clause.push_back(Var(true, std::string("c_" + std::to_string(i) + "_"
                                                            + std::to_string(k) + "_"
                                                            + std::to_string(j))));
            }
            if (!clause.empty()) cnf.push_back(clause);
        }
    }

    for (int i = n; i < n + N; i++) {
        for (int k = 0; k < 2; k++) {
            for (int j = i + 1; j < n + N; j++) {
                for (int l = i + 1; l < n + N; l++) {
                    Clause clause;
                    if (j == l) continue;
                    clause.push_back(Var(false, std::string("c_" + std::to_string(i) + "_"
                                                     + std::to_string(k) + "_"
                                                     + std::to_string(j))));
                    clause.push_back(Var(false, std::string("c_" + std::to_string(i) + "_"
                                                     + std::to_string(k) + "_"
                                                     + std::to_string(l))));
                }   
            }   
        }
    }

    // 3
    for (int i1 = n; i1 < n + N; i1++) {
        for (int i2 = n; i2 < n + N; i2++) {
            if (i1 < i2) {
                Clause clause;

                clause.push_back(Var(false, std::string("o_" + std::to_string(i1) + "_0")));
                clause.push_back(Var(false, std::string("o_" + std::to_string(i2) + "_0")));

                cnf.push_back(clause);
            }
        }
    }
    
    { 
        Clause clause;
        for (int i = n; i < n + N; i++) {
            clause.push_back(Var(true, std::string("o_" + std::to_string(i) + "_0")));
        } 

        cnf.push_back(clause);
    }

    // 4
    for (int i = 0; i < n; i++) {
        for (long long int t = 0; t < ttn.exp2n; t++) {
            Clause clause;

            clause.push_back(Var(ttn.Table_Lines[t][i], std::string("v_" + std::to_string(i) + "_"
                                                                         + ttn.to_string(t))));
            cnf.push_back(clause);
        }
    }    

    
    // 5
    for (int i = n; i < n + N; i++) {
        for (int j0 = 0; j0 < i; j0++) {
            for (int j1 = 0; j1 < i; j1++) {
                for (int i0 = 0; i0 < 2; i0++) {
                    for (int i1 = 0; i1 < 2; i1++) {
                        for (long long int r = 0; r < ttn.exp2n; r++) {
                            Clause clause1, clause2;

                            clause1.push_back(Var(false, std::string("c_" + std::to_string(i) + "_0_"
                                                                          + std::to_string(j0))));
                            clause1.push_back(Var(false, std::string("c_" + std::to_string(i) + "_1_"
                                                                          + std::to_string(j1))));

                            clause1.push_back(Var(!i0, std::string("v_" + std::to_string(j0) + "_"
                                                                        + ttn.to_string(r))));

                            clause1.push_back(Var(!i1, std::string("v_" + std::to_string(j1) + "_"
                                                                        + ttn.to_string(r))));

                            clause1.push_back(Var(false, std::string("v_" + std::to_string(i) + "_"
                                                                          + ttn.to_string(r))));
                            clause1.push_back(Var(true, std::string("t_" + std::to_string(i) + "_"
                                                                         + std::to_string(i0) + "_"
                                                                         + std::to_string(i1))));

                            clause2.push_back(Var(false, std::string("c_" + std::to_string(i) + "_0_"
                                                                          + std::to_string(j0))));
                            clause2.push_back(Var(false, std::string("c_" + std::to_string(i) + "_1_"
                                                                          + std::to_string(j1))));

                            clause2.push_back(Var(!i0, std::string("v_" + std::to_string(j0) + "_"
                                                                        + ttn.to_string(r))));

                            clause2.push_back(Var(!i1, std::string("v_" + std::to_string(j1) + "_"
                                                                        + ttn.to_string(r))));

                            clause2.push_back(Var(true, std::string("v_" + std::to_string(i) + "_"
                                                                          + ttn.to_string(r))));
                            clause2.push_back(Var(false, std::string("t_" + std::to_string(i) + "_"
                                                                         + std::to_string(i0) + "_"
                                                                         + std::to_string(i1))));
                            cnf.push_back(clause1);
                            cnf.push_back(clause2);
                        }
                    }
                }   
            }
        }
    } 

    // 6
    for (long long r = 0; r < ttn.exp2n; r++) {
        for (int i = n; i < n + N; i++) {
            Clause clause;

            clause.push_back(Var(false, std::string("o_" + std::to_string(i) + "_0")));
            clause.push_back(Var(f[ttn.Table_Lines[r]], std::string("v_" + std::to_string(i) + "_"
                                                                        + ttn.to_string(r))));

            cnf.push_back(clause);
        } 
    } 

    std::set<Var> var_set;
    
    // to miniSAT
    {

    int count = 1;
    std::unordered_map<std::string, int> var_names;

    for (long unsigned int i = 0; i < cnf.size(); i++) {
        for (Var &b : cnf[i]) {
            if (var_names.find(b.name) == var_names.end()) {
                var_names[b.name] = count;
                count++;
            }
            b.number = (b.sign ? var_names[b.name] : -1 * var_names[b.name]);
            var_set.insert(b);
        }
    }

    std::ofstream minisat_in;
    minisat_in.open("minisat_in");

    minisat_in << "p cnf " << var_names.size() << " " << cnf.size() << std::endl;
    for (Clause cls : cnf) {
        for (long unsigned int i = 0; i < cls.size() - 1; i++) {
            minisat_in << cls[i].number << " ";
        }
        minisat_in << cls[cls.size() - 1].number << " 0" << std::endl;
    }
   
    minisat_in.close();

    pid_t minisat_pid = fork();
    if (minisat_pid == -1) {
        std::cerr << "Fork failed" << std::endl;
        return 1;
    }
    
    if (minisat_pid == 0) {
        execl("/bin/minisat", "minisat", "minisat_in", "minisat_out", NULL);         
        std::cerr << "minisat failed" << std::endl;
        return 2;
    } 

    waitpid(minisat_pid, NULL, 0);

    } 

    // read minisat_out

    {
        std::ifstream minisat_out;
        minisat_out.open("minisat_out");
        
        std::string key;
        minisat_out >> key;
        if (key == "UNSAT") {
            std::cout << "No solutions" << std::endl;
            return 0;
        }

        for (auto &v : var_set) {
            int value;
            minisat_out >> value;
            if (value > 0) {
                Var new_var(v);
                new_var.value = true;  
                var_set.erase(v);
                var_set.insert(new_var);
            }
        } 

        minisat_out.close();
    }

//    for (Var v : var_set) {
//        std::cout << v.name << " = " << v.value << std::endl;
//    } 

 //   print_cnf(cnf); */

    // create and draw graph
    {

    Circuit c;

    c.set_vertexes(n, N, var_set);
    c.set_edges(n, N, var_set);
    //c.print_vertexes();
    //c.print_edges();

    std::ofstream circuit_gv;
    circuit_gv.open("circuit.gv");

    circuit_gv << "digraph Circuit {" << std::endl;
    c.print_edges(circuit_gv);
    circuit_gv << "}";
    circuit_gv.close();

    pid_t dot_pid = fork();
    if (dot_pid == -1) {
        std::cerr << "Fork failed" << std::endl;
        return 1;
    }

    if (dot_pid == 0) {
        execl("/bin/dot", "dot", "-Tpng", "circuit.gv", "-ocircuit.png", NULL);
        std::cerr << "dot failed" << std::endl; 
        return 2;
    }

    waitpid(dot_pid, NULL, 0);

    } 

    return 0;
}
