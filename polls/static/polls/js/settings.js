class Settings extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            // settings:this.props.settings,
            RESTRICTION_TYPES : ['none','oneKey','specialKeys'],
            show_keys_table:false,
            poll_name: this.props.settings.name,
            restrictionType:this.props.settings.restrictionType,
            closing_date:this.props.settings.closing_date,
            live_results: this.props.settings.live_results,
            groups:[],
            edit_groups:false,
            editing_group:"",
            keys:[],
        }  
    }
    render(){
        var restriction_selection = this.restriction_selection();
        var keys_table = this.display_keys_table();
        var display_groups = this.display_groups();
        if(!this.props.settings){
            return(<div></div>)
        };
        return(
            <div>
                <div className="container-center-row lone-btn" >
                {this.props.settings.is_active ? 
                    false
                :
                    <button className="btn btn-outline-primary btn-lg" name="edit_groups_button" onClick={this.handleClick}>
                        Groups
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-folder-minus" viewBox="0 0 16 16">
                            <path d="m.5 3 .04.87a1.99 1.99 0 0 0-.342 1.311l.637 7A2 2 0 0 0 2.826 14H9v-1H2.826a1 1 0 0 1-.995-.91l-.637-7A1 1 0 0 1 2.19 4h11.62a1 1 0 0 1 .996 1.09L14.54 8h1.005l.256-2.819A2 2 0 0 0 13.81 3H9.828a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 6.172 1H2.5a2 2 0 0 0-2 2zm5.672-1a1 1 0 0 1 .707.293L7.586 3H2.19c-.24 0-.47.042-.683.12L1.5 2.98a1 1 0 0 1 1-.98h3.672z"/>
                            <path d="M11 11.5a.5.5 0 0 1 .5-.5h4a.5.5 0 1 1 0 1h-4a.5.5 0 0 1-.5-.5z"/>
                        </svg>
                    </button>
                }
                </div>
                <div>
                    {this.state.edit_groups ?
                        <div className = "container-center-column container-overlay">
                            <div className="display-overlay">
                                <div>
                                    {this.state.groups.length < 3 ?
                                    <div className="form-row">
                                        <div className="form-group col-md-10">
                                            <input className="form-control" type="text" id="add_new_group_name" placeholder="Group Name"></input>
                                        </div>
                                        <div className="form-group col-md-2">
                                            <button className="btn btn-success" onClick={this.add_new_group}>Add Group</button>
                                        </div>
                                    </div>
                                    :
                                    false
                                    }
                                </div>
                                <br></br>

                                {display_groups}

                            </div>
                            <div className="container-center-row lone-btn">
                                <button className="btn btn-info btn-lg" style={{color:"white"}} onClick={this.handleClick} name="close_edit_groups">Close</button>
                            </div>
                        </div>   
                    :  
                    false}
                </div>

                <div className="container">
                    <div>
                        <p>Voting link : <a href={`${HOST}/polls/votingPage/${this.props.settings.name}/`}> {HOST}/polls/votingPage/{this.props.settings.name}/ </a></p>
                        {this.props.settings.hidden ?
                        <div>
                            <h3>Show</h3>
                        </div>
                        :
                        <h3>Hide</h3>
                        }
                        <div style={{width:"250px"}} >
                            <label className="switch">
                                <input type="checkbox" id="hide_poll_slider" onClick={()=>this.update_poll("hide")} defaultChecked={this.props.settings.hidden}></input>
                                <span className="slider round"></span>
                            </label>
                        </div>  
                    </div>
                    <br></br>


                    <div>
                        {this.props.settings.is_active ?
                            <h3>Deactivate</h3>
                        :
                            <h3>Activate</h3>
                        }
                        <div style={{width:"250px"}} >
                            <label className="switch">
                                <input type="checkbox" id="launch_poll_slider" onClick={()=>this.update_poll("launch")}  defaultChecked={this.props.settings.is_active}></input>
                                <span className="slider round"></span>
                            </label>
                        </div>  
                    </div>
                    <br></br>


                    {(this.props.settings.restrictionType === "oneKey" | this.props.settings.restrictionType === "specialKeys"  ) ?
                        <div>
                            <button className="btn btn-primary lone-btn" id="show_keys_table_btn" onClick={this.handleClick}>Show Keys</button>
                            <br></br>
                        </div>
                    :
                        false
                    }

                        <div>
                            <a className="btn btn-primary" href={`${HOST}/polls/results/${this.props.settings.name}/`}>RESULTS</a>
                        </div>
                    


                    {this.props.settings.is_active ?
                        false
                    :
                        <div>
                            <div style={{marginTop:"2em"}}>
                                <h2 className="text-center">Edit</h2>
                                <div className="form-group">
                                    <label>Name</label>
                                    <input className="form-control capitalize" type="text" name="poll_name" onChange={this.handleChange} defaultValue={this.props.settings.name}></input>
                                </div>
                                <br></br>

                                <div className="form-group">
                                    <label>Image</label>
                                    <input className="form-control-file" id="new_poll_image" name="image" type="file" ></input>              
                                </div>
                                <br></br>

                                <div className="form-group">
                                    <label>Restriction Trype: </label>
                                    <select className="form-control" id="restriction_selection" name="restriction_selection" onChange={this.handleChange} defaultValue={this.props.settings.restrictionType}>
                                        {restriction_selection}
                                    </select>
                                </div>
                                <br></br>

                                <div>
                                    {this.props.settings.restrictionType === "oneKey" ?
                                        <p style={{color:"yellow"}}>
                                            Keys are reusable
                                        </p>
                                        :
                                        
                                        false
                                    }
                                    {this.props.settings.restrictionType === "specialKeys" ?
                                        <p style={{color:"yellow"}}>
                                            Keys are not reusable
                                        </p>
                                        :
                                        false
                                    }
                                </div>
                                <br></br>

                                <div className="form-group">
                                    <label >Closing Date</label>
                                    <input className="form-control" type="date" name="closing_date" onChange={this.handleChange} defaultValue={this.props.settings.closing_date}/>                
                                </div>
                                <br></br>

                                <div className="form-group">
                                    <label > Show Live Results </label>
                                    <input  type="checkbox" name="live_results" onChange={this.handleChange} defaultChecked={this.props.settings.live_results}></input>
                                </div>
                                <br></br>


                                <div className="container-center-row lone-btn">
                                    <button className="btn btn-success btn-lg" onClick={this.submit_changes}>SAVE CHANGES</button>
                                </div>
                                <br></br>
                                <div className="container-center-row lone-btn">
                                    <button className="btn btn-danger" onClick={this.delete_poll}>DELETE POLL</button>
                                </div>
                            </div><br/>
                        </div>
                    }
                    
                    {this.state.show_keys_table ?
                        <div className = "container-center-column container-overlay">
                            <div className="display-overlay">

                                <div>
                                    <input type="text" className="form-control" id ="enter_new_key" placeholder="key"></input>
                                </div>
                                <div className="container-center-row lone-btn">
                                    <button className="btn btn-success" onClick={this.add_key} >SAVE KEY</button>
                                </div>

                                <div className="container-center-column lone-btn" style={{marginBottom:"3em"}}>
                                    <input style={{width:"120px"}}  className="form-control-file" id="excel_sheet_keys" type="file" accept="application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" />
                                    <br></br>
                                    <button className="btn btn-outline-primary btn-lg" onClick={this.upload_keys_excel}>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-file-earmark" viewBox="0 0 16 16">
                                            <path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z"/>
                                        </svg>
                                        Upload Keys(Excel)
                                    </button>
                                </div>

                                <div className="container-center-column lone-btn">
                                    <a  href={`${HOST}/polls/${this.props.settings.name}/Excelkeys/`}  className="btn btn-outline-primary btn-lg">
                                        Download Keys
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-file-earmark-arrow-down" viewBox="0 0 16 16">
                                            <path d="M8.5 6.5a.5.5 0 0 0-1 0v3.793L6.354 9.146a.5.5 0 1 0-.708.708l2 2a.5.5 0 0 0 .708 0l2-2a.5.5 0 0 0-.708-.708L8.5 10.293V6.5z"/>
                                            <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/>
                                        </svg>
                                    </a>
                                </div>

                                <br></br>

                                <table className="table">
                                    <thead className="thead-light">
                                        <tr>
                                            <th scope="col">key</th>
                                            <th scope="col">Used</th>
                                            <th scope="col">Remove</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                    {keys_table}
                                    
                                    </tbody>
                                </table>
                            
                            </div>
                            <div className="container-center-column lone-btn">
                                <button className="btn btn-info" id="close_keys_table_btn" onClick={this.handleClick}>CLOSE</button>
                            </div>
                        </div>
                    :
                        false
                    }
                </div>
            </div>
        )
    }
   
    componentDidMount=()=>{
        window.scrollTo(0, 0);
        if (this.props.settings) { 
            this.get_groups();
            this.get_keys();
        }
    }

    componentDidUpdate=(prevProps)=> {
        if (prevProps.settings !== this.props.settings) { 
            this.setState({
                poll_name: this.props.settings.name,
                restrictionType:this.props.settings.restrictionType,
                closing_date:this.props.settings.closing_date,
                live_results: this.props.settings.live_results,
            });
            this.get_groups();
            this.get_keys();
        }
    }

    get_groups=()=>{
        fetch(`${HOST}/polls/getGroups/${this.props.settings.name}/`)
        .then(response => response.json())
        .then(response=>{
            this.setState({
                groups:response,
            })
        })
        .catch(err=>{
            console.error(err)
        })
    }

    display_groups=()=>{
        var groups = this.state.groups.map(group=>{
            var editing = false;
            if(this.state.editing_group === group.name){
                editing = true;
            }
            return(
                <Group key={group.id} group={group} editing={editing} change_group_editing={this.change_group_editing} update_poll={this.update_poll} delete={this.delete_group}/>
            )
        })
        return groups
    }

    restriction_selection=()=>{
        var res_type = this.state.RESTRICTION_TYPES.map((type,index)=>{ 
            return(
                <option key={index} value = {type} className="form-control">{type}</option>
            )
        })
        return res_type
    }

    
    handleChange=(event)=>{
        if(event.target.name === "restriction_selection" ){
            if(confirm("Changing restriction type can lead to loss of key(s) data, do you wish to proceed?")){
                this.setState({
                    restrictionType:event.target.value
                })
            }else{
                event.target.value = this.props.settings.restrictionType
            }
        }
        else if(event.target.name === "poll_name" ){
            this.setState({
                poll_name:event.target.value
            }) 
        }
        else if(event.target.name === "closing_date" ){
            //console.log("change closing date",event.target.value)
            this.setState({
                closing_date:event.target.value
            }) 
        }
        else if(event.target.name === "live_results" ){
            //console.log(event.target.checked)
            this.setState({
                live_results:event.target.checked
            }) 
        } 
    }

    handleClick=(event)=>{
        if(event.target.id === "show_keys_table_btn" ){
            this.setState({
                show_keys_table:true
            })
        }
        else if(event.target.id === "close_keys_table_btn" ){
            this.setState({
                show_keys_table:false
            })
        }
        else if(event.target.name === "edit_groups_button" ){
            this.setState({
                edit_groups:true
            })
        }
        else if(event.target.name === "close_edit_groups" ){
            this.setState({
                edit_groups:false
            })
            this.change_group_editing()
        }
    }

    update_poll=(action,group_id,group_new_name)=>{
        //console.log(action)
        var element =""
        var activity =""
        var message = "Do you wnat to save changes?"
        if(action === "hide"){
            element = document.getElementById("hide_poll_slider")
            activity = element.checked
            message = "Hidden polls will not be seen by other users when active, CONTINUE ?"
        }
        else if(action === "launch"){
            element = document.getElementById("launch_poll_slider")
            activity = element.checked
            message = "This may delete all previous data, CONTINUE ? "
        }

        if(confirm(message)){
            fetch(`${HOST}/polls/${this.props.settings.name}/management/settings/`,{
                method:"PUT",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    "id" : this.props.settings.id,
                    "action" : action,
                    "activity": activity,
                    "group_id" : group_id,
                    "group_new_name":group_new_name
                }),
            })
            .then(response=>{
                this.props.get_settings()
                // //console.log(response.status)
                if(response.status === 400){
                    element.checked = !element.checked
                    return response.json()
                }
                if(group_new_name){
                    this.change_group_editing()
                }
            })
            .then(response=>{
                if(response){
                    alert(response.error)
                }
            })
            .catch(err=>{
                console.error(err)
            })
        }else{
            element.checked = !element.checked
        }
    }

    submit_changes=()=>{
        if(confirm("Submit Changes ?")){
            var image = document.getElementById("new_poll_image")
            const form_data = new FormData()

            if(image.files[0]){
                form_data.append("image",image.files[0])
            }else{
                //console.log("no image chosen")
            }
            form_data.append("action","edit_poll")
            form_data.append("name",this.state.poll_name)
            form_data.append("restrictionType",this.state.restrictionType)
            form_data.append("closing_date",this.state.closing_date)
            form_data.append("live_results",this.state.live_results)

            fetch(`${HOST}/polls/${this.props.settings.name}/management/settings/`,{
                method:'POST',
                mode:'same-origin',
                headers: {
                    "Accept":"application/json",
                    "X-Requested-With":'XMLHttpRequest',
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body:form_data,
            })
            .then(response=>{
                if(response.status === 201){
                    // this.props.get_settings(this.state.poll_name)
                    const BASE_URL = `${HOST}/polls/manage/${this.state.poll_name}`
                    window.history.pushState("x","xx",`${BASE_URL}/settings/`)
                }
                window.location.href = window.location.href
            })
            .catch(err=>{
                console.error(err)
            })
        }
    }

    delete_poll=()=>{
        if(confirm("Do you want to delete poll?")){
            fetch(`${HOST}/polls/${this.props.settings.name}/management/settings/`,{
                method:"DELETE",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    "action":"poll"
                }),
            })
            .then(response=>{
                if(response.status == 201){
                    window.location = HOST
                }
            })
        }
    }

    add_new_group=()=>{
        const name = document.getElementById("add_new_group_name").value
        //console.log(name)
        const form_data = new FormData()
        form_data.append("action","new_group")
        form_data.append("name",name)

        fetch(`${HOST}/polls/${this.props.settings.name}/management/settings/`,{
            method:'POST',
            mode:'same-origin',
            headers: {
                "Accept":"application/json",
                "X-Requested-With":'XMLHttpRequest',
                "X-CSRFToken": getCookie("csrftoken")
            },
            body:form_data,
        })
        .then(response=>{
            this.get_groups()
            document.getElementById("add_new_group_name").value = ""
        })
        
    }

    delete_group=(group_name)=>{
        if(confirm("Do you want to delete group?")){
            fetch(`${HOST}/polls/${this.props.settings.name}/management/settings/`,{
                method:"DELETE",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    "name" : group_name,
                    "action":"group"
                }),
            })
            .then(response=>{
                this.get_groups()
            })
        }
    }

    change_group_editing=(name)=>{
        if(name){
            this.setState({
                editing_group:name
            })
        }else{
            this.setState({
                editing_group:""
            })
        }
        this.get_groups()
    }
    
    get_keys=()=>{
        fetch(`${HOST}/polls/${this.props.settings.name}/management/keys/`)
        .then(response => response.json())
        .then(response=>{
            this.setState({
                keys:response,
            })
            //console.log(response)
        })
    }

    display_keys_table=()=>{
        var keys = this.state.keys.map(key=>{
            return(
                <Key key={key.id} access_key={key} delete={this.delete_key}/>
            )
        })
        return keys
    }
    

    add_key=()=>{
        const key = document.getElementById("enter_new_key").value.trim()
        if(!key){
            return //console.log("eneter a key")
        }
       
        if(confirm("Do you want to add new key?")){
            fetch(`${HOST}/polls/${this.props.settings.name}/management/keys/`,{
                method:"POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    "key":key,
                }),
            })
            .then(response=>{
                this.get_keys()
            })
            document.getElementById("enter_new_key").value = ""
        }
    }

    delete_key=(key_id)=>{
        if(confirm("Do you want to delete key?")){
            fetch(`${HOST}/polls/${this.props.settings.name}/management/keys/`,{
                method:"DELETE",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    "key_id":key_id
                }),
            })
            .then(response=>{
                this.get_keys()
            })
        }
    }

    upload_keys_excel=()=>{
        if(confirm("Proceed to add excel keys(first column)?")){
            const sheet = document.getElementById("excel_sheet_keys")
            const form_data = new FormData()

            if(sheet.files[0]){
                form_data.append("sheet",sheet.files[0])
                fetch(`${HOST}/polls/${this.props.settings.name}/Excelkeys/`,{
                    method:'POST',
                    mode:'same-origin',
                    headers: {
                        "Accept":"application/json",
                        "X-Requested-With":'XMLHttpRequest',
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body:form_data,
                })
                .then(response=>{
                    this.get_keys()
                })
            }
        }
    }
}

class Group extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            new_name : ""
        }  
    }
    render(){
        return(
            <div>
                {this.props.editing ?
                    <div>
                        <input className="form-control" onChange={this.handleChange} name="group_name" type='text' defaultValue={this.props.group.name}></input><br/>
                        
                        <div className="container-center-row lone-btn">
                            <button className="btn btn-success btn-lg" onClick={this.save_changes}>Save</button><br/>
                        </div>

                        <div className="container-center-row lone-btn">
                            <button className="btn btn-danger btn-lg" onClick={()=>this.props.delete(this.props.group.name)}>Delete</button><br/>
                        </div>
         
                    </div>

                :
                <div>
                    <h2 style={{textTransform:"capitalize"}}> {this.props.group.name}</h2>
                    <button className="btn btn-primary btn-lg" onClick={()=>{this.props.change_group_editing(this.props.group.name)}}>Edit</button>
                </div>
                }
                <br/>
            </div>
        )
    }

    save_changes=()=>{
        if(this.state.new_name.trim()){
            this.props.update_poll('edit_group',this.props.group.id,this.state.new_name)
        }
        this.props.change_group_editing()
    }

    handleChange=(event)=>{
        if(event.target.name === "group_name"){
            this.setState({
                new_name:event.target.value
            })
        }
    }
}


class Key extends React.Component{
    constructor(props){
        super(props)  
        this.state={
           
        }  
    }

    render(){
        return(
        <tr>
            <td scope="col">{this.props.access_key.key}</td>
            {this.props.access_key.used?
                <td scope="col">Yes</td>
            :
                <td scope="col">No</td>
            }
            <td scope="col"><button className="btn btn-danger" onClick={()=>this.props.delete(this.props.access_key.id)}>REMOVE</button></td>
        </tr>
        )
    }

}
