const base_url = window.location.href.substring(0,25)
const new_user=new Vue({
    el:'#app.dashboard',
    data() {
        return {
            myprofile: myprofile,
            pass_stren:false,
            image: null,
        }
    },
    methods: {
        'load_friends':function(){
            fetch(`${base_url}/api/connection/${this.myprofile.user_id}`,{
                method:"GET"
            })
            .then((res)=>{if(res.ok){return res.json()}
                        else{console.log('result',res.text);throw new Error(res.text())}})
            .then((data)=>{sessionStorage.setItem('conn_list',JSON.stringify(data.connection))})
            .catch((err)=>{console.log(err.message);})
            },
            dashBoard:function () {
                window.location.href=`${base_url}/dashboard/${this.myprofile.user_id}`
            },
        },
    created:function() {
        sessionStorage.setItem('myprofile',JSON.stringify(myprofile))
        this.load_friends()
    }
})