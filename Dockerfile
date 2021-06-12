FROM "continuumio/miniconda3"

RUN apt-get update && yes | apt-get upgrade

RUN mkdir FeatureEncoder

COPY .. /FeatureEncoder/

WORKDIR /FeatureEncoder/

RUN conda env create -f restyle_env.yaml

RUN apt-get install -y git python-pip

RUN pip install --upgrade pip

RUN apt-get install -y protobuf-compiler python-pil python-lxml

RUN pip install jupyter

RUN pip install matplotlib





RUN export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

RUN jupyter notebook --generate-config --allow-root

RUN echo "c.NotebookApp.password = u'sha1:6a3f528eec40:6e896b6e4828f525a6e20e5411cd1c8075d68619'" >> /root/.jupyter/jupyter_notebook_config.py

EXPOSE 8885

CMD ["jupyter", "notebook", "--allow-root", "--notebook-dir=/FeatureEncoder/", "--ip=0.0.0.0", "--port=8885", "--no-browser"]