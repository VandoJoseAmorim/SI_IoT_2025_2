ROTEIRO AULA 05
Prof. Massaki
INSTALE O ANACONDA PYTHON
Link: https://www.anaconda.com/download/success
▶️ Dicas para instalação: https://vimeo.com/724995785
[![Assista ao vídeo no Vimeo](THUMBNAIL_URL)](https://vimeo.com/724995785)
*Clique na imagem para abrir o vídeo no Vimeo.*

#Para atualizar versão do Python:
python -V
#Após ter o Python instalado, o próximo passo é verificar se o Pip já está instalado em seu sistema. Para isso, abra o terminal ou prompt de comando e digite o seguinte comando: pip --version
pip --version

#Para atualizar versão do instalador pip:
pip3 -V
pip3 install --upgrade pip

#Para atualizar o Anaconda
conda update -n base -c defaults conda
# conda create --name <env_name> python=3.8
conda create --name python python=3.12
conda activate python
##3.12.3
conda create --name python=3.12.3
# To activate this environment, use
conda activate streamlit
#     $ conda activate streamlit
#
# To deactivate an active environment, use
#
#     $ conda deactivate

conda update -n base -c defaults conda
python -m pip install streamlit
python -m streamlit hello
python -m streamlit run app.py
pip install streamlit --upgrade
python -m pip install --upgrade pip
python.exe -m pip install --upgrade pip
conda create --name python310 python=3.10

pip3 install -r requirements.txt 
ou 
python -m pip install -r requirements.txt

Os Packages ficam em
c:\users\massa\.conda\envs\python\lib\site-packages
[notice] A new release of pip is available: 24.0 -> 24.1.1
[notice] To update, run: python.exe -m pip install --upgrade pip

python -m pip install --upgrade pip


 
Passo 1
pip3 install --upgrade pip
Passo 2
python -m pip install -r requirements.txt
