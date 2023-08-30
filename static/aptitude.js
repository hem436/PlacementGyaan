const base_url = window.location.href.substring(0,25)

const all_post = new Vue({
    el:"#app",
    data(){
        return{
        myprofile:JSON.parse(sessionStorage.getItem('myprofile')),
        conn_list:JSON.parse(sessionStorage.getItem('conn_list')),
        apti_list:[],
        quest_list:[],
        currentPage:1,
        }
    },
    computed: {
    },
    methods: {
        editApti:function(){
            sessionStorage.setItem('currentPost',JSON.stringify(this.currentPost))
            window.location.href=`${base_url}/edit_apti`
        },
        dashBoard:function () {
            window.location.href=`${base_url}/dashboard/${this.myprofile.user_id}`
        },
        mergeArray:function(){
            const idToQuest = {};
            for (const obj of this.quest_list) {
                idToQuest[obj.apti_id] = obj.questions;
            }

            // Update list1 with marks from list2
            for (const obj of this.apti_list) {
                if (idToQuest[obj.apti_id] !== undefined) {
                obj.questions = idToQuest[obj.apti_id];
                }
            }
        },
        load_quest:function(apti_id) {
            fetch(`${base_url}/api/apti/${apti_id}/test_q/0`),{
                method:"GET"
            }
            .then((res)=>{if(res.ok){return res.json()}
                        else{throw new Error(res.text())}})
            .then((data)=>{
                this.quest_list.push(data.quest_obj)
            })
            .catch((err)=>{console.log(err.message)})
        },
        load_apti:function(){
            fetch(`${base_url}/api/0/apti/${this.myprofile.user_id}`,{
                method:"GET"
            })
            .then((res)=>{if(res.ok){return res.json()}
                        else{throw new Error(res.text())}})
            .then((data)=>{
                data.aptis.forEach(element=>{
                    this.apti_list.push(element)
                    this.load_quest(element.apti_id)
                })
                
            })
            .catch((err)=>{ console.log(err.message);})
            
            if(this.conn_list.length > 0){
                this.conn_list.forEach(element => {
                    fetch(`${base_url}/api/0/apti/${element}`,{
                    method:"GET"
                })
                .then((res)=>{if(res.ok){return res.json()}
                            else{console.log(res.text());}})
                .then((data)=>{
                    data.aptis.forEach(element=>{
                        this.post_list.push(element)
                    })
                })
                .catch((err)=>{ console.log(err.message);})
                });
            }
        },
        'deleteApti':function(){
            fetch(`${base_url}/api/apti/${this.currentPost.apti_id}`,{
                method:"DELETE",
            })
            location.reload()
        },
    },
    created(){
        this.load_post()
        console.log('posts',this.post_list)
    },
})
