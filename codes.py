example1_iner = """#This is an example for A+B problem...'
var_t = [randint(1, 10) for i in range(0, 1)]
for i in range(0, 1):
	write("%d "%(var_t[i]))
write('\\n')
var_2 = [[randint(1, 100) for i in range(0, 2)] for j in range(0, var_t[0])]
for i in range(0, var_t[0]):
	for j in range(0, 2):
		write("%d "%(var_2[i][j]))
	write("\\n")
"""
example1_sol = """#include<iostream>
using namespace std;
int a, b;
int main(){
    int t; cin >> t;
    while(t--){
        cin >> a >> b;
        cout << a + b << endl;
    }
    return 0;
}
"""
example2_iner = """#This is an example for Luogu P1005...
var_t = [randint(4, 7) for i in range(0, 2)]
for i in range(0, 2):
	write("%d "%(var_t[i]))
write('\\n')
var_1 = [[randint(1, 100) for i in range(0, var_t[1])] for j in range(0, var_t[0])]
for i in range(0, var_t[0]):
	for j in range(0, var_t[1]):
		write("%d "%(var_1[i][j]))
	write("\\n")
"""
example2_sol = """#include<bits/stdc++.h>
#define in(x) x=read()
#define MAXN 81
#define k m-(R-L)
#define bll __int128
using namespace std;
inline int read() 
{
    int X=0,w=1;
    char ch=getchar();
    while(ch<'0' || ch>'9') {if(ch=='-') w=-1;ch=getchar();}
    while(ch>='0' && ch<='9') X=(X<<3)+(X<<1)+ch-'0',ch=getchar();
    return X*w;
}
int n,m;
int num[MAXN];
bll ans,p[MAXN],f[MAXN][MAXN];
bll dp(int L,int R)
{
    if(f[L][R]!=-1) return f[L][R];
    if(R-L>=1) f[L][R]=max(num[L]*p[k]+dp(L+1,R),dp(L,R-1)+num[R]*p[k]);
    else f[L][R]=num[L]*p[k];
    return f[L][R];
}
void print(bll x)
{
    if(!x) return;
    if(x) print(x/10);
    putchar(x%10+'0');
}
int main()
{
    in(n);in(m);
    p[0]=1;
    for(int i=1;i<=m;i++) p[i]=p[i-1]*2;
    for(int i=1;i<=n;i++)
    {
        for(int j=1;j<=m;j++) in(num[j]);
        memset(f,-1,sizeof(f));
        ans+=dp(1,m);
    }
    if(!ans) printf("0");
    else print(ans);
    return 0;
}
//By windows250
"""
#path->null
iner_head = """from random import *
import string
path = "G://vsc//testmaker//"
f = open(path + "tin.txt", "w")
def write(s: str):
    f.write(s)
"""
iner_tail = """
f.close()
"""
sol_insert = """
    freopen("{path}tin.txt", "r", stdin);
    freopen("{path}tout.txt", "w", stdout);
"""
dp_insert = """
    freopen("{path}tin.txt", "r", stdin);
    freopen("{path}pout.txt", "w", stdout);
"""
add_int_1 = """{var_name} = [randint({mi}, {ma}) for i in range(0, {num})]
if {random_mode} == 1:
    {var_name}.sort()
elif {random_mode} == -1:
    {var_name}.sort(reverse = True)
for i in range(0, {num}):
    write("%d{sep}"%({var_name}[i]))
"""
add_int_2 = """{var_name} = [[randint({mi}, {ma}) for i in range(0, {y})] for j in range(0, {x})]
if {random_mode} == 1:
    for row in {var_name}:
        row.sort()
elif {random_mode} == -1:
    for row in {var_name}:
        row.sort(reverse = True)
for i in range(0, {x}): 
    for j in range(0, {y}):
        write("%d{sep}"%({var_name}[i][j]))
    write("\\n")
"""
add_var_1 = """{var_name} = [randint({mi}, {ma}) for i in range(0, {num})]
if {random_mode} == 1:
    {var_name}.sort()
elif {random_mode} == -1:
    {var_name}.sort(reverse = True)
"""
add_var_2 = """{var_name} = [[randint({mi}, {ma}) for i in range(0, {y})] for j in range(0, {x})]
if {random_mode} == 1:
    for row in {var_name}:
        row.sort()
elif {random_mode} == -1:
    for row in {var_name}:
        row.sort(reverse = True)
"""
add_str_1 = """char_set = "{extra}"+string.digits*{have_123}+string.ascii_lowercase*{have_abc}+string.ascii_uppercase*{have_ABC}
for i in range(0, {num}):
    rand_str = "".join(sample(char_set, randint({mi}, {ma})))
    write("%s{sep}"%(rand_str))
"""
add_str_2 = """char_set = "{extra}"+string.digits*{have_123}+string.ascii_lowercase*{have_abc}+string.ascii_uppercase*{have_ABC}
for i in range(0, {num}):
    rand_str = ""
    for j in range(0, randint({mi}, {ma})):
        rand_str = rand_str + choice(char_set)
    write("%s{sep}"%(rand_str))
"""
add_enter = """write("\\n")
"""
add_space = """write(" ")
"""