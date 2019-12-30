import boto3 # importing framework for AWS
from boto3.session import Session
from azure.storage.blob import *
from azure.storage.blob._blob_client import *
from azure.storage.blob._blob_service_client import * #importing framework for Microsoft AZURE
from flask import *#importing python flask
import os
from google.cloud import storage #importing framework for Google-cloud

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


sc = Session(aws_access_key_id='Accesskey', aws_secret_access_key='secretkey')#assigning acceskey & secret key of Goolgle-cloud for accessing thecloud account


app = Flask(__name__)


@app.route('/')
def firstpage():
    return render_template('main.html') #this html page allows the user to choose the cloud service providers


# Amazon Cloud Management
@app.route('/amazon')
def list():
    return render_template('s3_first_main.html')#this html page  asks user to select either external bucket or internal bucket operation should be done


@app.route('/buck')
def mainrun():
    return render_template('s3_main.html')#this html page displays external bucket operations


@app.route('/blist')
def blist():
    s3 = boto3.resource('s3')#accesing all resources of S3 storage
    a = []
    for bucket in s3.buckets.all():
        a.append(bucket.name)
    return render_template('s3_your_view.html', your_list=a)#this page displays list of buckets existing in S3 storage


@app.route('/suc')
def open_suc():
    return render_template('s3_succ.html')# this page allows the user to create the new bucket


@app.route('/cbuck', methods=['POST'])
def cbuck():
    b_name = request.form['bn']
    item = b_name
    try:
        process = 'It is successfully created'
        s3 = boto3.resource('s3')
        s3.create_bucket(Bucket=b_name, CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
        return render_template('s3_common.html', item=item, process=process)
    except:
        process = 'It is already available,change the name of the bucket'
        return render_template('s3_common.html', item=item, process=process)


@app.route('/del')
def bdel():
    return render_template('s3_dval.html')# this page allows the user to the delete the existing bucket



@app.route('/delete', methods=['POST'])#the post method used to get data from html page
def dele():
    try:
        d_name = request.form['d_val']
        item = d_name
        process = 'It is deleted successfully'
        s3 = boto3.client('s3')
        s3.delete_bucket(Bucket=d_name)
        return render_template('s3_common.html', item=item, process=process)
    except:
        item = request.form['d_val']
        process = 'It is unavailable or Check the name or internet '
        return render_template('s3_common.html', item=item, process=process)

#internal bucket operation in AWS
@app.route('/bfile')
def file():
    return render_template('s3_mainf.html')#this html page displays internal bucket operations
@app.route('/listf')
def cf():
    return render_template('s3_upf.html')


@app.route('/createf', methods=['POST'])
def create():
    sf = request.form['sf']
    db = request.form['db']
    df = request.form['df']
    item = sf
    try:
        process = 'It is uploaded successfully'
        s3 = boto3.client('s3')
        s3.upload_file(sf, db, df)
        return render_template('s3_common.html', item=item, process=process)
    except:
        process = 'It is not uploaded,try again later or check the values'
        return render_template('s3_common.html', item=item, process=process)


@app.route('/lf')
def call():
    return render_template('s3_listf.html')


@app.route('/pfile', methods=['POST'])
def printfile():
    a = []
    b_name = request.form['bname']
    try:
        s3 = sc.resource('s3')
        buck = s3.Bucket(b_name)
        for s3_f in buck.objects.all():
            a.append(s3_f.key)
        return render_template('s3_your_view.html', your_list=a)
    except:
        item = b_name
        return render_template('s3_common.html', item=item,
                               process=' check the name of the bucket  or internet connection')


@app.route('/dfile')
def lf():
    return render_template('s3_dfval.html')


@app.route('/dfile', methods=['POST'])
def listing():
    b_name = request.form['bname']
    f_name = request.form['fname']
    item = f_name
    try:
        process = 'It is deleted successfully'
        client = boto3.client('s3')
        client.delete_object(Bucket=b_name, Key=f_name)
        return render_template('s3_common.html', item=item, process=process)
    except:
        return render_template('s3_common.html', item=item, process='It is not deleted,check the connection or value')


@app.route('/df')
def down():
    return render_template('s3_dfile.html')


@app.route('/downf', methods=['POST'])
def downloadfile():
    process = 'It is downloaded successfuly'
    b_name = request.form['bname']
    f_name = request.form['fname']
    d_name = request.form['dname']
    item = f_name
    try:
        s3 = boto3.client('s3')
        s3.download_file(b_name, f_name, d_name)
        return render_template('s3_common.html', item=item, process=process)
    except:
        return render_template('s3_common.html', item=item, process='check the value')


# Google Cloud Management
@app.route('/gcloud')
def main():
    return render_template('gmain.html')#this html page  asks user to select either external bucket or internal bucket operation should be done


@app.route('/external')
def external():
    return render_template("gexternal.html")#this html page displays external bucket operations


@app.route('/internal')
def internal():
    return render_template("ginternal.html")#this html page displays internal bucket operations


@app.route('/bcreate')
def create1():
    return render_template('gcreate.html')


@app.route('/upload')
def upload():
    return render_template('gupload.html')


@app.route('/download')
def download():
    return render_template('gdownload.html')


@app.route('/delete')
def delete():
    return render_template('gdelete.html')


@app.route('/deletef')
def deletef():
    return render_template('gdeletef.html')


@app.route('/listfile')
def listfile():
    return render_template("glist.html")



@app.route('/created', methods=['POST'])
def created():
    if request.method == 'POST':
        bucket_name = request.form['bucket']
        storage_client = storage.Client()
        bucket = storage_client.create_bucket(bucket_name)
        return render_template("gfinal.html", sol="It is created successfully", val=bucket_name)



@app.route('/uploaded', methods=['POST'])
def uploaded():
    try:

        if request.method == 'POST':
            bucket_name = request.form["bucket"]
            sfile = request.form["sfile"]
            dfile = request.form["dfile"]
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(dfile)
            blob.upload_from_filename(sfile)
            return render_template("gfinal.html", sol="uploaded successfully", val=sfile)
    except:
        return render_template("gfinal.html", sol="It is unable to upload", val=sfile)


@app.route('/downloaded', methods=['POST'])
def downloaded():
    try:
        if request.method == 'POST':
            sfile = request.form["sfile"]
            dfile = request.form["dfile"]
            bucket_name = request.form["bucket"]
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(sfile)
            blob.download_to_filename(dfile)
            return render_template("gfinal.html", sol="is downloaded successfully", val=sfile)
        # return "{} is file downloaded".format(sfile)
    except:
        return render_template("gfinal.html", sol="It is unable to download.Please check the file is in the bucket",
                               val=sfile)


@app.route('/deleted', methods=['POST'])
def deleted():
    try:
        if request.method == 'POST':
            bucket_name = request.form["bucket"]
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
            bucket.delete()
            return render_template("gfinal.html", sol="is deleted sucessfully.", val=bucket_name)
            # return "{} bucket is deleted".format(bucket_name)
    except:
        return render_template("gfinal.html", sol="It is unable to delete . Please check the bucket name.",
                               val=bucket_name)


@app.route('/deletefile', methods=['POST'])
def deletefile():
    try:
        if request.method == 'POST':
            bucket_name = request.form["bucket"]
            sfile = request.form["sfile"]
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(sfile)
            blob.delete()
            return render_template("gfinal.html", sol="is deleted successfully", val=sfile)

            # return "{} file is deleted".format(sfile)
    except:
        return render_template("gfinal.html", sol="It is unable to delete.Please check the file is in the bucket. ",
                               val=sfile)


@app.route('/listed')
def listed():
    try:
        storage_client = storage.Client()
        buckets = storage_client.list_buckets()
        b = []
        for bucket in buckets:
            b1 = (bucket.name)
            b.append(b1)
        return render_template("gprintlist.html", lis=b)

    except:
       return render_template("final.html",val="Sorry",sol="Unable to list the bucket")


@app.route('/listf', methods=['POST'])
def listf():
    n = list()
    try:
        if request.method == 'POST':
            bucket_name = request.form["bucket"]

            storage_client = storage.Client()

            blobs = storage_client.list_blobs(bucket_name)

            for blob in blobs:
                n1 = blob.name
                n.append(n1)
            return render_template("gprintlist.html", lis=n)
    except:
        return "please valid details"


# Microsoft Azure

@app.route('/azure')
def azure():
    return render_template("azuremain.html")#this html page  asks user to select either external bucket or internal bucket operation should be done


#external operations
@app.route('/aexternal')
def aexternal():
    return render_template("azureexternal.html")

#internal operations
@app.route('/ainternal')
def ainternal():
    return render_template("azureinternal.html")


# EXTERNAL
@app.route('/acreate')
def acreate():
    return render_template("acreate.html")


@app.route('/adelete')
def adelete():
    return render_template("adelete.html")


# IINTERNAL
@app.route('/alistfile')
def alist():
    return render_template("alist.html")


@app.route('/aupload')
def aupload():
    return render_template("aupload.html")


@app.route('/adownload')
def adownload():
    return render_template("adownload.html")


@app.route('/adeletefile')
def adeletefile():
    return render_template("adeletefile.html")


# operation
@app.route('/acreated', methods=['POST'])
def acreated():
    global container_name
    try:
        container_name = request.form["container"]
        container_client = blob_service_client.create_container(container_name)
        return render_template("afinal.html", sol="It is succesfully created", val=container_name)
    except:
        return render_template("afinal.html", sol="Sorry,Unable to create(please give unique name)", val=container_name)


@app.route('/adeleted', methods=['POST'])
def adeleted():
    try:
        container_name = request.form["container"]
        container_client = ContainerClient.from_connection_string(conn_str=connect_str, container_name=container_name)
        container_client.delete_container()
        return render_template("afinal.html", sol="It is successfully deleted", val=container_name)
    except:
        return render_template("afinal.html", sol="Sorry,Unable to delete(Please check the Container name)")


@app.route('/alisted')
def alisted():
    block_blob_service = BlobServiceClient(account_url="accounturl",
                                           credential="credential ")# these variables can be varied for different users, must be checked before execution of the program

    containers = block_blob_service.list_containers()
    c2 = []
    for c in containers:
        c1 = c.name
        c2.append(c1)
    return render_template("aprintlist.html", lis=c2)


# operation internal
@app.route('/alistfile', methods=['POST'])
def alistfile():
    try:
        container_name = request.form["container"]
        container = ContainerClient.from_connection_string(conn_str=connect_str, container_name=container_name)

        blob_list = container.list_blobs()
        blobs1 = []
        for blob in blob_list:
            blobs1.append(blob.name)
        return render_template('aprintlist.html', lis=blobs1)
    except:
        return render_template("afinal.html", sol="Sorry,Unable to list the blobs (Please check the Container name)")


@app.route('/auploaded', methods=['POST'])
def auploaded():
    try:
        container_name = request.form["container"]
        #sfile = request.form["sfile"]
        dfile = request.form["dfile"]
        filename=os.path.basename(dfile)
        foldername=dfile.strip("/"+filename)
        local_path = foldername
        local_file_name = filename

        upload_file_path = os.path.join(local_path, local_file_name)

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)



        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)

        return render_template("afinal.html", val=filename, sol="It is uploaded successfully")
    except:
        return render_template("afinal.html", sol="Sorry,Unable to upload(Please check the Container name)")


@app.route('/adownloaded', methods=['POST'])
def adownloaded():
    try:
        container_name = request.form["container"]
        sfile = request.form["sfile"]
        dfile = request.form["dfile"]
        blob = BlobClient.from_connection_string(conn_str=connect_str, container_name=container_name,
                                                 blob_name=sfile)
        with open(dfile, "wb") as my_blob:
            blob_data = blob.download_blob()
            blob_data.readinto(my_blob)
        return render_template("afinal.html", val=sfile, sol="It is downloaded Successfully")
    except:
        return render_template("afinal.html",
                               sol="Sorry,Unable to download(Please check the Container name,Source filename )")


@app.route('/adeletef', methods=['POST'])
def adeletef():
    try:
        container_name = request.form["container"]
        sfile = request.form["sfile"]
        container = ContainerClient.from_connection_string(conn_str=connect_str, container_name=container_name)
        container.delete_blob(sfile)
        return render_template("afinal.html", val=sfile, sol="It is deleted Successfully")
    except:
        return render_template("afinal.html",
                               sol="Sorry,Unable to delete(Please check the Container name,Source filename )")


if __name__ == '__main__':
    app.run()#finally running the python Flask
