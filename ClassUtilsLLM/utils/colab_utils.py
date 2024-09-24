import pickle
import pickle
import datetime
from google.colab import files

def get_app_name():
    try:
        # Check if running in IPython or Jupyter Notebook
        shell = get_ipython()
        if shell:
            # Get the filename of the current notebook
            return shell.findCaller()[1]
    except:
      # Not running in IPython or Jupyter Notebook
      try:
        return __file__
      except:
        pass
    # Return None if not in IPython or Jupyter Notebook
    return ''
class Backup():
  def __init__(self,read_from=None,savename=None):
    self.savename=savename
    if read_from is None:
      self.backup = {}
    else:
      self.read_backup(read_from)
  def set(self,name,value):
    self.backup[name] = value
  def download(self,filename=None,dont_download=False,download_all_state=False):
    if self.savename is None:
      if filename is None:
        application_name = '_'+get_app_name()
        current_datetime = '_'+str(datetime.datetime.now())
        filename = f'backup{application_name}{current_datetime}'
    else:
      filename = self.savename
    filename+='.pkl'

    with open(filename, 'wb') as f:
      if not download_all_state:
        pickle.dump(self.backup, f)
      else:
        pickle.dump(globals(),f)
    if not dont_download:
      files.download(filename)

  def read_backup(self,filename,atualize_vars=True):
    if not '.pkl' in filename:
      filename += '.pkl'
    with open(filename, 'rb') as arquivo:
      self.backup = pickle.load(arquivo)
    if atualize_vars:
      self.atualize_vars()
  def atualize_vars(self):
    for name,value in self.backup.items():
      globals()[name] = value








## Classe que funciona como um backup simples (ideia: ela ser herdada para as próximas classes)
class Savable():
  def save(self,download=True):
      obj_compact = pickle.dumps(self)
      with open(self.name, 'wb') as f:
          f.write(obj_compact)
      if download:
        files.download(self.name)
  @staticmethod
  def open(filename): ##modo de uso: experiment1 = Savable.open('experiment1.pkl')
    with open(filename, 'rb') as f:
      obj_compact = f.read()
      obj = pickle.loads(obj_compact)
    return obj


if __name__ == "__main__":
  class Aluno(Savable):
    def __init__(self, nome, idade, matricula,name="batata"):
        self.name=name
        self.nome = nome
        self.idade = idade
        self.matricula = matricula
    
    def __str__(self):
        return f"Nome: {self.nome}, Idade: {self.idade}, Matrícula: {self.matricula}"
  
  # Instanciando um objeto aluno
  aluno1 = Aluno("João", 20, "2021001")

  # Mostrando informações do aluno
  print(aluno1)
  aluno1.save(download=True)
  aluno2 = Savable.open('batata')
  print(aluno2)