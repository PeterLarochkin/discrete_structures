#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <set>
#include <fstream>


class Atom {
public:
    bool sign;
    std::string value;
    Atom(int _sign, const std::string& _value):
        sign(_sign), value(_value) {}
    Atom(bool _sign, const std::string& _value):
        sign(_sign), value(_value) {}
    Atom(const Atom& a):
        sign(a.sign), value(a.value) {}
};

std::string str(int a) {
    return "_" + std::to_string(a);
}

bool bit(int pos, int num) {
    for (int i = 0; i < pos; i++) num >>= 1;
    return num & 1;
}

bool value(int pos, int input, std::vector<std::vector<bool>> func) {
    const auto& result = func[input];
    return result[pos];
}

std::string operator+(const std::string& a, const std::string& b) {
    return a + "_" + b;
}

std::string operator+(const std::string& a, int n) {
    return a + "_" + std::to_string(n);
}

std::string operator+(int n, const std::string& b) {
    return std::to_string(n) + "_" + b; 
}

long long int exp2_(int n) {
    long long int result = 1;
    for (int i = 0; i < n; i++) {
        result *= 2;
    }
    return result;
}

void draw(const std::vector<Atom> vect) {
    const auto r_ = *vect.rbegin();
    std::cerr << (!r_.sign ? "-" : " ") << r_.value << " ";
}

void br() {
    std::cerr << std::endl;
}

void rb() {
    std::cerr << "";
}

int main(int nargs, char** args) {
    int n;
    int N;
    int m; 

    std::cin >> n;

    std::cin >> N;

    std::cin >> m;

    long long int exp2n = exp2_(n);
    std::vector<std::vector<bool>> target_func(exp2n);

    for (int i = 0; i < exp2n; i++) {
        std::string lin;
        std::cin >> lin;
        for (auto a: lin) {
           target_func[i].push_back(a-'0');
        }
    }
    
    // Initializing basis - c_i means that i-th gate is a &, d_i - that it is a V, etc.
    // Here we ensure that every gate has only one assigned function
    std::vector<std::vector<Atom>> cnf;

    for (int i = n; i < n + N; i++) {
        for (int a = 0; a < 2; a++) {
        for (int b = 0; b < 2; b++) {
        for (int c = 0; c < 2; c++) {
            if (a+b+c == 2) continue;
            std::vector<Atom> res; br(); 
            res.push_back(Atom(a, "n"+ str(i))); draw(res);
            res.push_back(Atom(b, "d"+ str(i))); draw(res);
            res.push_back(Atom(c, "C"+ str(i))); draw(res);
            cnf.push_back(res); rb();
        }}}
    }

    // Here we OR all the possible functions of the gates. If a gate is N, it has the corresponding t, etc.
    for (int i = n ; i < n + N; i++  ) {
    for (int b0 = 0; b0 < 2;    b0 ++) {
    for (int b1 = 0; b1 < 2;    b1 ++) {
        std::vector<Atom> res1; br();
        res1.push_back(Atom(0, "n"+str(i))); draw(res1);
        res1.push_back(Atom(!b0, "t"+str(i)+str(b0)+str(b1))); draw(res1);
        cnf.push_back(res1); rb();

        std::vector<Atom> res2; br();
        res2.push_back(Atom(0, "d"+str(i))); draw(res2);
        res2.push_back(Atom(b0 || b1, "t"+str(i)+str(b0)+str(b1))); draw(res2);
        cnf.push_back(res2); rb();

        std::vector<Atom> res3; br();
        res3.push_back(Atom(0, "C"+str(i))); draw(res3);
        res3.push_back(Atom(b0 && b1, "t"+str(i)+str(b0)+str(b1))); draw(res3);
        cnf.push_back(res3); rb();
    }}}

    // we ensure that at for every gate and it's input, at least one upstream gate is connected 
    
    for (int i = n; i < n + N; i++) {
    for (int k = 0; k < 2    ; k++) {
        std::vector<Atom> res; br();
        for (int j = 0; j < i; j++) {
            res.push_back(Atom(1, "c"+str(i)+str(k)+str(j))); draw(res);
        }
        if (!res.empty()) cnf.push_back(res); rb();
    }}

/*
    for (int i = 0; i < N + n; i++) {
        for (int j = 0; j < N+n; j++) {
            for (int k = 0; k < 2; k++) {
                if (j < i) continue;
                std::vector<Atom> res; br();
                res.push_back(Atom(0, "c"+str(i)+str(k)+str(j))); draw(res);
                cnf.push_back(res); rb();
            }
        }
    }
*/
/*
    for (int i = n; i < n+N; i++)  {
        
    }
*/
    // for each non-input gate there's at least one gate fed by it; except outputs
/*    for (int j = n; j < n+N-m; j++) {
        std::vector<Atom> res; br();
        for (int i = n; i < n + N; i++) {
            for (int k = 0; k < 2; k++) {
            res.push_back(Atom(1, "c"+str(i)+str(k)+str(j))); draw(res);
    }   }
        cnf.push_back(res); rb();
    }
*/

    // and that the connected gate is the only one for every gate input
    for (int i = n; i < n + N; i++) {
    for (int k = 0; k < 2;       k++) {
    for (int j = i+1; j < n+N;   j++) {
        for (int l = i+1 ; l < n+N; l++) {
            std::vector<Atom> res; br();
            if (l == j) continue;
            res.push_back(Atom(0, "c"+str(i)+str(k)+str(j))); draw(res);
            res.push_back(Atom(0, "c"+str(i)+str(k)+str(l))); draw(res);
            cnf.push_back(res); rb();
        }
    }}}

    // ensure each output is connected to a gate
    for (int j = 0; j < m; j++) {
            std::vector<Atom> res; br();
        for (int i = n; i < n + N ; i++) {
            res.push_back(Atom(1, "o"+str(i)+str(j))); draw(res);
        }
            cnf.push_back(res); rb();
    }

    //ensure that no two gates are connected to the same output
    for (int j = 0; j < m; j++) {
    for (int i = n; i < n+N; i++) {
        for (int l = n; l < n+N; l++) {
            if (l == i) continue;
            std::vector<Atom> res; br();
            res.push_back(Atom(0, "o"+str(i)+str(j))); draw(res);
            res.push_back(Atom(0, "o"+str(l)+str(j))); draw(res);
            cnf.push_back(res); rb();
        }
    }}

    // v_i_t for i < n equals i-th bit of the number t
    for (int i = 0; i < n; i++) {
    for (int t = 0; t < exp2n; t++) {
        std::vector<Atom> res; br();
        res.push_back(Atom(bit(i, t), "v"+str(i)+str(t))); draw(res);
        cnf.push_back(res); rb();
    }}

    // each gate computes the composition of the function of the previous gates
    for (int i = n   ; i < n + N ; i++)  {
    for (int j0 = 0  ; j0 < i    ; j0++)  {
    for (int j1=0 ; j1 < i    ; j1++) {
    for (int i0 = 0  ; i0 < 2    ; i0++) {
    for (int i1 = 0  ; i1 < 2    ; i1++) {
    for (int r = 0   ; r < exp2n ; r++)  {
///        if (j0 == j1 && j0 >=n && j1 >= n) continue;
        std::vector<Atom> res; br();
        res.push_back(Atom(0, "c"+str(i)+"_0"+str(j0))); draw(res);
        res.push_back(Atom(0, "c"+str(i)+"_1"+str(j1))); draw(res);
        ///
        res.push_back(Atom(!i0, "v"+str(j0)+str(r))); draw(res);
        res.push_back(Atom(!i1, "v"+str(j1)+str(r))); draw(res);
    /*
        std::vector<Atom> res1;
        res1.push_back(Atom(1, "v"+str(i)+str(r)));
        res1.push_back(Atom(0, "t"+str(i)+str(i0)+str(i1)));
        cnf.push_back(res1);
*/
        res.push_back(Atom(0, "v"+str(i)+str(r))); draw(res);
        res.push_back(Atom(1, "t"+str(i)+str(i0)+str(i1))); draw(res);
        ///std::cout << "res" << res2[1].value;
        cnf.push_back(res); rb();

        std::vector<Atom> re; br();
        re.push_back(Atom(0, "c"+str(i)+"_0"+str(j0))); draw(re);
        re.push_back(Atom(0, "c"+str(i)+"_1"+str(j1))); draw(re);
        ///
        re.push_back(Atom(!i0, "v"+str(j0)+str(r))); draw(re);
        re.push_back(Atom(!i1, "v"+str(j1)+str(r))); draw(re);
    
        re.push_back(Atom(1, "v"+str(i)+str(r))); draw(re);
        re.push_back(Atom(0, "t"+str(i)+str(i0)+str(i1))); draw(re);
        cnf.push_back(re); rb();
/*
        std::vector<Atom> re2;
        re2.push_back(Atom(0, "v"+str(i)+str(r)));
        re2.push_back(Atom(1, "t"+str(i)+str(i0)+str(i1)));
        ///std::cout << "res" << res2[1].value;
        cnf.push_back(re2);
*/
    }}}}}}

    // the outputs compute the correct function
    for (int k = 0; k < m; k++) {
    for (int r = 0; r < exp2n; r++) {
    for (int i = n; i < n + N; i++) {
        std::vector<Atom> res; br();
        res.push_back(Atom(0, "o"+str(i)+str(k))); draw(res);
        res.push_back(Atom(value(k, r, target_func), "v"+str(i)+str(r))); draw(res);
        cnf.push_back(res); rb();
    }}}


    std::vector<std::vector<long int>> true_cnf;
    long int count = 1;
    std::unordered_map<std::string, long int> variable_names;


    for (int i = 0; i < cnf.size(); i++) {
        std::vector<long int> true_cnf_dis;
        for (auto b: cnf[i]) {
            if (variable_names.find(b.value) == variable_names.end()) {
                variable_names[b.value] = count;
                count++;
                ///std::cout << "auto b: cnf[i: setting variable_name[" << b.value << "] to " << count-1 << std::endl;
            }
            ///std::cout << "b_value__" << b.value << " " << count << std::endl;
            true_cnf_dis.push_back(b.sign==0 ? -1*variable_names[b.value] : variable_names[b.value]);
        }
        true_cnf.push_back(true_cnf_dis);
    }

    std::set<std::pair<long int, std::string>> s;
    for (auto i: variable_names) {
    s.insert(std::make_pair(i.second, i.first));
    }

    std::ofstream vars;
    vars.open("vars");
    vars << n << " " << N << " " << m << " ";
    for (auto i: s) {
        //std::cerr << i.first << ":::" << i.second << "   ";
        vars << i.second << "  ";
    }

    std::cout << "p cnf " << variable_names.size() << " " << true_cnf.size() << std::endl;
    for (auto i: true_cnf) {
        for (int b = 0; b < i.size()-1; b++){
            std::cout << i[b] << " ";
            //std::cerr << i[b] << " ";
        }
        std::cout << i[i.size()-1] << " 0" << std::endl;
        //std::cerr << i[i.size()-1]  << std::endl;
    }
    ///////////////////////////////////////////////////////
    
    /*
    SATSolver solver;
    solver.set_num_threads(6);
    solver.new_vars(count-1)
    std::vector<CMSat::Lit> clause;
    count = 0;
    for (int i = 0; i < cnf.size(); i++) {
        clause.clear()
        for (auto b: cnf[i]) {
            clause.push_back(CMSat::Lit(variable_names[b.value]-1, b.sign));
        }
        solver.add_clause(clause);
    }
    //Let's use 4 threads

    lbool ret = solver.solve();
    assert(ret == l_True);
    std::cout
    << "Solution is: "
    << solver.get_model()[0]
    << ", " << solver.get_model()[1]
    << ", " << solver.get_model()[2]
    << std::endl;
*/
}
