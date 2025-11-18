from ronglian_sms_sdk import SmsSDK

accId = '2c94811c9860a9c4019951720af0288d'
accToken = '777ffda66b7b45baa3250378561bfd25'
appId = '2c94811c9860a9c401995179ad492897'  #为上线

# def send_message():
#     sdk = SmsSDK(accId, accToken, appId)
#     tid = '1'
#     mobile = '18379309798'
#     datas = ('3456', '5')
#     resp = sdk.sendMessage(tid, mobile, datas)
#     print(resp)
#############################################################################################

sdk = SmsSDK(accId, accToken, appId)
def send_sms_codes(mobile,sms_code):
    datas = (sms_code, '5')
    sdk.sendMessage(tid='1',datas=datas,mobile=mobile)

if __name__ == '__main__':
    send_sms_codes(mobile='18379309798',sms_code='1234')