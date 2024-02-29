from flask import Flask, jsonify,request
import job_datas
import math
app = Flask(__name__)


@app.route('/get_job',)
def rot():
    page = request.args.get('page_num', type=int)
    loc = request.args.get('location', type=str)
    
    val=job_datas.job_data(loc,math.ceil(page/5))
    num=page%5
    start=(num)*5
    end=(num+1)*5
    if val!=None: 
        return val[start:end]
    else:
        return []



@app.route('/get_job_details', methods=['GET'])
def get_audio_details():
    job_name = request.args.get('job_name', type=str)
    loc = request.args.get('location', type=str)
    job_type = request.args.get('job_type', type=str)
    job_exp = request.args.get('job_exp', type=str)
    job_loc = request.args.get('job_loc', type=str)
    gen = request.args.get('when_generated', type=str)
    page_num = request.args.get('page_num', type=int)
    details=job_datas.start(job_name,loc,job_type,job_exp,page_num,job_loc,gen)
    print(details)
    num=page_num%5
    start=(num)*5
    end=(num+1)*5

    # job_data=[]
    # for detail in details:
    #     for job in detail:
    #         job_data.append(job)
    
    # return jsonify(job_data)
    if details!=None:
        return jsonify(details[start:end])
    else:
        return []
if __name__=="__main__":
    app.run() 

