// 此处我选择的是vue3的导入方法

// 创建vue应用
// const {createApp} = Vue
const app = Vue.createApp({
    el: '#app',
    // 修改vue的语法
    delimiters: ['[[',']]'],

    data(){
        return {
            // 1. v-model 部分
            username:'',
            password:'',
            password2:'',
            mobile:'',
            allow:'',
            // 2. v-show 部分
            error_name:false,
            error_password:false,
            error_password2:false,
            error_mobile:false,
            error_allow:false,
            // 3. error_message
            error_name_message:'',
            error_mobile_message:'',

        }

        },
            // 4. 事件部分
    methods: {
        // 4.1 校验用户名
        check_username(){
            // 用户名是5-20个字符 [a-zA-Z0-9]{5:20}
            // 斜杠用于包裹正则的 “匹配模式”，明确告诉 JavaScript 引擎：“中间的内容是正则表达式，不是普通字符串”。
            let re_name = /^[a-zA-Z0-9_-]{5,20}$/;
            if(re_name.test(this.username)){
                // 匹配成功，不显示错误信息
                this.error_name = false;
            }else{
                // 匹配失败返回错误信息
                this.error_name_message = '请输入5-20个字符的用户名'
                this.error_name = true;
            }
        },
        // 4.2 校验密码
        check_password(){
            let re_password = /^[a-zA-Z0-9]{8,20}$/
            if(re_password.test(this.password)){
                this.error_password = false;
            }else{
                this.error_password = true;
            }
        },
        // 4.3 检验确认密码
        check_password2(){
            let re_password2 = /^[a-zA-Z0-9_-]{5,20}$/;
            if(re_password2.test(this.password2) && this.password2 === this.password2){
                this.error_password2 = false;
            }else {
                this.error_password2 = true;
            }
        },
        // 4.4 校验手机号
        check_mobile(){
            let re_mobile = /^[1-9]{2}[0-9]{9}$/
            if(re_mobile.test(this.mobile)){
                this.error_mobile = false;
            }else {
                this.error_mobile_message = '请输入正确的手机号码'
                this.error_mobile = true;
            }
        },
        // 4.5校验是否勾选协议
        check_allow(){
            if(this.allow){
                this.error_allow = false;
            }else{
                this.error_allow = true;
            }
        },
        // 4.6 监听表单提交事件
        on_submit(){
            // 现在对以上的函数事件进行校验，通过执行函数，data中的数据会得到改变
            this.check_username()
            this.check_password()
            this.check_password2()
            this.check_mobile()
            this.check_allow()

            // 只要有一个数据为true，即：有错误信息得到了展示，就要阻止表单提交
            if(this.error_name === true || this.error_password === true ||
                this.error_password2 === true || this.error_mobile === true || this.error_allow === true){
                window.event.returnValue = false;
            }
        },
    }
});app.mount('#app');
// 通过id选择器找到绑定的HTML内容

