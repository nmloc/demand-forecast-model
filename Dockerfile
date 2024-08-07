FROM python:3.10.2

COPY json_to_df.py json_to_df.py
COPY model.pkl model.pkl

WORKDIR /

# Install necessary packages
RUN pip install pandas scikit-learn

ENTRYPOINT [ "bash" ]


