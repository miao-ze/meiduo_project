let vm = new Vue({
    el: "#app",

    // 修改Vue读取变量的模板语法
    delimiters: ['[[', ']]'],

    data: {
        // v-model
        uuid: '',
        image_code_url: '',
        username: '',
        password: '',
        confirm_pwd: '',
        image_code: '',
        mobile: '',
        sms_code: '',
        sms_code_tip: '获取短信验证码',
        send_flag: false,   // 短信发送标记
        register_errmsg: '',
        allow: false,

        // v-show
        error_username: false,
        error_password: false,
        error_confirm_pwd: false,
        error_mobile: false,
        error_allow: false,
        error_image_code: false,
        error_sms_code: false,

        // 控制展示注册时的错误信息
        show_register_errmsg: false,

        // error_msg
        error_username_msg: '',
        error_mobile_msg: '',
        error_image_code_msg: '',
        error_sms_code_message: '',

    },

    // 页面加载完成后执行
    mounted() {
        // 生成图形验证码
        this.generate_image_code();
    },

    methods: {
        generate_image_code() {
            // 生成UUID。generateUUID() : 封装在common.js文件中，需要提前引入
            this.uuid = generateUUID();
            // 拼接图形验证码请求地址
            this.image_code_url = "/image_codes/" + this.uuid + "/";

        },
        check_username() {
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_username = false;
            } else {
                this.error_username_msg = '请输入5-20个字符的用户名';
                this.error_username = true;
            }

            if (this.error_username === false) {
                // 判断用户名是否重复注册
                let url = '/usernames/' + this.username + '/count/'
                let options = {responseType: 'json'}
                axios.get(url, options)
                    .then(response => {
                        if (response.data.count === 1) {
                            this.error_username_msg = '用户名已存在';
                            this.error_username = true;
                        } else {
                            this.error_username = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },
        check_password() {
            let re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        check_confirm_pwd() {
            if (this.password !== this.confirm_pwd) {
                this.error_confirm_pwd = true;
            } else {
                this.error_confirm_pwd = false;
            }
        },
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;

            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_msg = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }

            if (this.error_mobile === false) {
                // 校验手机号是否重复注册
                let url = '/mobiles/' + this.mobile + '/count/'
                let options = {responseType: 'json'}
                axios.get(url, options)
                    .then(response => {
                        console.log(response.data)

                        if (response.data.count === 1) {
                            //    手机号重复注册
                            this.error_mobile = true
                            this.error_mobile_msg = '手机号码重复注册'
                        } else {
                            this.error_mobile = false
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },
        check_image_code() {
            if (this.image_code.length !== 4 ) {
                this.error_image_code_msg = '请填写图片验证码';
                this.error_image_code = true;
            } else {
                this.error_image_code = false;
            }
        },
        check_allow() {
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },
        check_sms_code() {
            if (!this.sms_code) {
                this.error_sms_code_message = '请填写短信验证码';
                this.error_sms_code = true;
            } else {
                this.error_sms_code = false;
            }
        },
        // 4.7发送邮箱（短信）验证码
        send_sms_code(){
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            // 设计一个可以使用容联云平台的测试手机号
            if (this.mobile === '18379309798'){
                // 从这里开始要重新进行构建
                  // 要避免恶意用户频繁的点击获取短信验证码的标签
            if(this.send_flag === true){ //当厕所的门是关的（已经有人在里面了），就不进去（就进行return，不执行下面的代码）
                return;
            }
            this.send_flag = true; //表示进来之后马上关门
            // 检验数据：this.email 和 this.image_code (因为用户可能在没有填写邮箱账户和图形验证的情况之下点击发送邮箱验证码)
            this.check_mobile();
            this.check_image_code();
            if(this.error_email === true || this.error_image_code === true){ // 如果有一个是有错误的就不继续执行下去
                this.send_flag = false;
                return;
            }
            // url中传入查询字符串，和后端逻辑进行配合使用，这里的字符串设置依据是后端的接受设置
            let url = '/sms_codes/miao/'+ this.mobile +'/?image_code=' + this.image_code +'&uuid=' + this.uuid;
            axios.get(url,{responseType:'json'})
            .then(response=>{
                if(response.data.code === '0'){
                // 显示倒计时60s效果
                    let num = 60;
                    let t =setInterval(() =>{
                        if (num === 0){ // 倒计时结束时
                            // 1.停止回调函数
                            clearInterval(t);
                            // 2.还原email_code_tip的显示文字
                            this.sms_code_tip = '获取验证码';
                            // 3.重新生成图形验证码
                            this.generate_image_code();
                            this.send_flag = false;  // 进行解锁，上完厕所后打开门
                        }else{ // 正在倒计时
                            num -= 1;
                            this.sms_code_tip = num + '秒';
                        }
                    },1000)
                }else{
                    if(response.data.code === '4001'){
                        // 图形验证码错误
                        this.error_image_code_msg = response.data.errmsg;
                        this.error_image_code = true;
                    }else{//短信验证码错误 4002
                        this.error_sms_code_message = response.data.errmsg
                        this.error_sms_code = true;
                    }
                    this.send_flag = false;
                }
            })
            .catch(error=>{
                console.log(error.response);
                this.send_flag = false;
            })
            }
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            else{
               // 要避免恶意用户频繁的点击获取短信验证码的标签
            if(this.send_flag === true){ //当厕所的门是关的（已经有人在里面了），就不进去（就进行return，不执行下面的代码）
                return;
            }
            this.send_flag = true; //表示进来之后马上关门
            // 检验数据：this.email 和 this.image_code (因为用户可能在没有填写邮箱账户和图形验证的情况之下点击发送邮箱验证码)
            this.check_mobile();
            this.check_image_code();
            if(this.error_email === true || this.error_image_code === true){ // 如果有一个是有错误的就不继续执行下去
                this.send_flag = false;
                return;
            }
            // url中传入查询字符串，和后端逻辑进行配合使用，这里的字符串设置依据是后端的接受设置
            let url = '/sms_codes/'+ this.mobile +'/?image_code=' + this.image_code +'&uuid=' + this.uuid;
            axios.get(url,{responseType:'json'})
            .then(response=>{
                if(response.data.code === '0'){
                    alert('验证码：' + response.data.sms_code);
                // 显示倒计时60s效果
                    let num = 60;
                    let t =setInterval(() =>{
                        if (num === 0){ // 倒计时结束时
                            // 1.停止回调函数
                            clearInterval(t);
                            // 2.还原email_code_tip的显示文字
                            this.sms_code_tip = '获取验证码';
                            // 3.重新生成图形验证码
                            this.generate_image_code();
                            this.send_flag = false;  // 进行解锁，上完厕所后打开门
                        }else{ // 正在倒计时
                            num -= 1;
                            this.sms_code_tip = num + '秒';
                        }

                    },1000)
                }else{
                    if(response.data.code === '4001'){
                        // 图形验证码错误
                        this.error_image_code_msg = response.data.errmsg;
                        this.error_image_code = true;
                    }else if(response.data.code === '4008'){//短信验证码错误 4002
                        this.error_sms_code_message = response.data.errmsg
                        this.error_sms_code = true;
                    }else{
                        this.error_sms_code_message = response.data.errmsg
                        this.error_sms_code = true;
                    }
                    this.send_flag = false;
                }
            })
            .catch(error=>{
                console.log(error.response);
                this.send_flag = false;
            })
            }
        },
        on_submit() {
            this.check_username();
            this.check_password();
            this.check_confirm_pwd();
            this.check_mobile();
            this.check_allow();
            //发送axios请求来判断短信验证码是否正确
            // let url = '/check_sms_codes/'+this.mobile+'/?sms_code='+this.sms_code;
            // axios.get(url,{responseType:'json'})
            //     .then(response=>{
            //         if(response.data.code === '0'){
            //             this.error_sms_code = false;
            //         }else{
            //             this.error_sms_code_message = response.data.errmsg;
            //             this.error_sms_code = true;
            //         }
            //     })
            //     .catch(error=>{
            //         console.log(error.response);
            //     })
            if (this.error_username === true || this.error_password === true || this.error_confirm_pwd === true
                || this.error_mobile === true || this.error_allow === true || this.error_sms_code === true ) {
                // 禁用表单的提交
                // alert('验证码输入错误')
                window.event.returnValue = false;
                console.log('args error')
            } else {
                console.log('register')
            }
        },
    },


})