import numpy as np
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n + 1))  # Inicializar com n + 1 elementos

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_y] = root_x

def group_connections(N): ## retorna um dicionário que relaciona cada grupo a um item (a partir dos dados)
    N_shape = np.array(N).shape
    mapping = {idx:i+1 for i,idx in enumerate(np.unique(np.reshape(np.array(N),-1)))}
    antimapping = {i:idx for idx,i in mapping.items()}
    # print(f"mapping: {mapping}")
    # print(f"antimapping: {antimapping}")

    N_mapped = np.reshape([mapping[idx] for idx in np.reshape(np.array(N),-1)],N_shape)
    # print(f"N_mapped: {list(N_mapped)}")

    max_vertex = max(max(edge) for edge in N_mapped)
    uf = UnionFind(max_vertex)
    for edge in N_mapped:
        uf.union(*edge)
    groups = {}
    for i in range(1, max_vertex + 1):  # Começar de 1
        root = uf.find(i)
        if root not in groups:
            groups[root] = []
        groups[root].append(i)

    mapped_groups = list(groups.values())
    # print(f"mapped_groups: {mapped_groups}")
    unmapped_groups = []
    for mapped_group in mapped_groups:
      unmapped_groups.append([antimapping[i] for i in mapped_group])
    return unmapped_groups

def group_antimapping(groups): ## retorna um dicionário que relaciona cada item a um grupo (a partir de um dicinário de grupos)
  antimapping = {}
  for group,items in groups.items():
    for item in items:
      antimapping[item] = group
  return antimapping




class MustLinkKMeans():
    def __init__(self, n_clusters, max_iters=0, tol=1e-4, random_state=None,cluster_centers=None):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.tol = tol
        self.random_state = random_state
        self.cluster_centers_ = cluster_centers

    def fit(self, X,ml=[]):
        # print("X shape: ",X.shape)
        if self.random_state:
            np.random.seed(self.random_state)


        # print("must link requerido: ",ml)
        in_ml = np.unique(np.reshape(np.array(ml),-1)) ## terminar e proibir os indices que estão no in_ml de mudarem
        # print(f"dados: {np.arange(len(X))}")
        # print("quantidade de dados linkados: ",(in_ml))

        # Inicialização dos grupos
        if len(ml)==0:
          self.groups = []
        else:
          self.groups = group_connections(ml)
        groups_centers = [np.mean(X[group],axis=0) for group in self.groups]
        # print(f"n_groups: {len(groups_centers)}  groups: {self.groups}")


        ## Sumariza os grupos como dados únicos e substituí pelos dados dos grupos

        X_excluded = list(X[[i for i in np.arange(0,len(X)) if i not in in_ml]])
        IDXexcluded2real = {idx_real:i for i,idx_real in enumerate(np.arange(len(X))[[i for i in np.arange(0,len(X)) if i not in in_ml]])}
        # print("IDXexcluded2real: ",IDXexcluded2real)


        # true_labels_aux = list(true_labels[[i for i in np.arange(0,len(X)) if i not in in_ml]])
        i_groups = len(X_excluded)
        # print("len X_excluded: ",i_groups)
        index2groups = {}
        for i,(group,icc) in enumerate(list(zip(self.groups,groups_centers))):
          X_excluded.append(icc)
          index2groups[i+i_groups] = group
        X_excluded = np.array(X_excluded)
        # print(f"index2groups: {index2groups}")
        # print(f"X_excluded (final) shape: {np.array(X_excluded).shape}")



        # Inicialização dos centróides
        idxs_min = []
        if self.cluster_centers_ is None:
          idxs_choiced = np.random.choice(X_excluded.shape[0], self.n_clusters, replace=False)
          self.cluster_centers_ = list(X_excluded[idxs_choiced])
          idxs_min = idxs_choiced
        else:
          self.cluster_centers_ = list(self.cluster_centers_)
        self.cluster_centers_ = np.array(self.cluster_centers_)
        # print("idxs_min: ",idxs_min)



        ## Fazendo o KMeans de fato
        for i in range(self.max_iters):
            # Cálculo das distâncias de cada ponto a cada cluster
            distances = np.linalg.norm(X_excluded[:, np.newaxis] - self.cluster_centers_, axis=2)

            # Atribução das labels
            self.labels_ = np.argmin(distances, axis=1)

            # Atualizar os centróides
            new_centers=[]
            for j in np.unique(self.labels_):
              new_centers.append(np.mean(X_excluded[self.labels_ == j], axis=0))
            new_centers = np.array(new_centers)

            # Verificar convergência
            # print(f"new_centers: {new_centers.shape}  self.cluster_centers_: {self.cluster_centers_.shape}\n\n")
            # if np.linalg.norm(new_centers - self.cluster_centers_) < self.tol:
            #     print(f"Break de convergência ativado na {i} iteração!!!")
            #     break

            self.cluster_centers_ = new_centers

        self.labels_with_groups = self.labels_.copy()


        g_antimapping = group_antimapping(index2groups)
        # print(f"ant label {len(self.labels_)}: {self.labels_}")
        # print('group: ',index2groups)
        # print('antimapping: ',g_antimapping)
        labels = [100] * len(X)
        for i in np.arange(len(X)):
          if i in g_antimapping.keys():
            labels[i] = self.labels_[g_antimapping[i]]
          else:
            # print(f"Não sei o que fazer no índice {i}")
            # print(f"    >> copiei o índice {IDXexcluded2real[i]} do self.labels_, que é {self.labels_[IDXexcluded2real[i]]}")
            labels[i] = self.labels_[IDXexcluded2real[i]]

        self.labels_ = labels
        self.X_with_groups = X_excluded
