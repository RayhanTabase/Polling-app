class CategoriesMgt extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            groups:[],
            categories : [],
            add_category: false,
            error_message:"",
            new_category:{
                name:"",
                group:"",
            },
            query:""
        }  
    }

    render(){
        var categories = this.display_categories()
        var group_selection = this.group_selection()
        if(!this.props.poll_name){
            return(<div></div>)
        }
        return(
            <div className="container">
                <div className="container-center-row lone-btn" >
                    {this.props.is_active ? 
                        false
                    :
                        <button className="btn btn-outline-primary btn-lg" name="add_category_button" onClick={this.handleClick}>
                            Add Category
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-plus-circle-dotted" viewBox="0 0 16 16">
                                <path d="M8 0c-.176 0-.35.006-.523.017l.064.998a7.117 7.117 0 0 1 .918 0l.064-.998A8.113 8.113 0 0 0 8 0zM6.44.152c-.346.069-.684.16-1.012.27l.321.948c.287-.098.582-.177.884-.237L6.44.153zm4.132.271a7.946 7.946 0 0 0-1.011-.27l-.194.98c.302.06.597.14.884.237l.321-.947zm1.873.925a8 8 0 0 0-.906-.524l-.443.896c.275.136.54.29.793.459l.556-.831zM4.46.824c-.314.155-.616.33-.905.524l.556.83a7.07 7.07 0 0 1 .793-.458L4.46.824zM2.725 1.985c-.262.23-.51.478-.74.74l.752.66c.202-.23.418-.446.648-.648l-.66-.752zm11.29.74a8.058 8.058 0 0 0-.74-.74l-.66.752c.23.202.447.418.648.648l.752-.66zm1.161 1.735a7.98 7.98 0 0 0-.524-.905l-.83.556c.169.253.322.518.458.793l.896-.443zM1.348 3.555c-.194.289-.37.591-.524.906l.896.443c.136-.275.29-.54.459-.793l-.831-.556zM.423 5.428a7.945 7.945 0 0 0-.27 1.011l.98.194c.06-.302.14-.597.237-.884l-.947-.321zM15.848 6.44a7.943 7.943 0 0 0-.27-1.012l-.948.321c.098.287.177.582.237.884l.98-.194zM.017 7.477a8.113 8.113 0 0 0 0 1.046l.998-.064a7.117 7.117 0 0 1 0-.918l-.998-.064zM16 8a8.1 8.1 0 0 0-.017-.523l-.998.064a7.11 7.11 0 0 1 0 .918l.998.064A8.1 8.1 0 0 0 16 8zM.152 9.56c.069.346.16.684.27 1.012l.948-.321a6.944 6.944 0 0 1-.237-.884l-.98.194zm15.425 1.012c.112-.328.202-.666.27-1.011l-.98-.194c-.06.302-.14.597-.237.884l.947.321zM.824 11.54a8 8 0 0 0 .524.905l.83-.556a6.999 6.999 0 0 1-.458-.793l-.896.443zm13.828.905c.194-.289.37-.591.524-.906l-.896-.443c-.136.275-.29.54-.459.793l.831.556zm-12.667.83c.23.262.478.51.74.74l.66-.752a7.047 7.047 0 0 1-.648-.648l-.752.66zm11.29.74c.262-.23.51-.478.74-.74l-.752-.66c-.201.23-.418.447-.648.648l.66.752zm-1.735 1.161c.314-.155.616-.33.905-.524l-.556-.83a7.07 7.07 0 0 1-.793.458l.443.896zm-7.985-.524c.289.194.591.37.906.524l.443-.896a6.998 6.998 0 0 1-.793-.459l-.556.831zm1.873.925c.328.112.666.202 1.011.27l.194-.98a6.953 6.953 0 0 1-.884-.237l-.321.947zm4.132.271a7.944 7.944 0 0 0 1.012-.27l-.321-.948a6.954 6.954 0 0 1-.884.237l.194.98zm-2.083.135a8.1 8.1 0 0 0 1.046 0l-.064-.998a7.11 7.11 0 0 1-.918 0l-.064.998zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
                            </svg>
                        </button>
                    }
                </div><br/>
                <div className="container-center-row">
                    <div className="search-box" style={{width:"90%"}}>    
                        <input className="form-control" id="query_input" type="text" placeholder="filter"></input>
                        <button type="submit" name="search_button" onClick={this.query_categories}><i className="form-control fa fa-search"></i></button>   
                    </div>
                </div>
                <div className="index row">
                    {categories}
                </div>

                <div>
                    {this.state.add_category ?
                        <div className = "container-center-column container-overlay">
                            <div className="display-overlay">
                                <form>
                                    <div className="form-group">
                                        <label>Name</label>
                                        <input className="form-control form_input capitalize" type="text" name="category_name" size='80' onChange={this.handleChange}></input>
                                    </div>
                                    <div className="form-group">
                                        <label>Group</label>
                                        <select className="form-control form_input" name="category_group" onChange={this.handleChange}>
                                            <option className="form-control" >None</option>
                                            {group_selection}
                                        </select>
                                    </div>
                                    <div className="container-center-row lone-btn">
                                        <button type="button" className="btn btn-lg btn-success" style={{color:"white"}} onClick={this.add_category}>Add</button>
                                    </div>
                                </form>
                                <div className="container-center-row lone-btn">
                                    <button className="btn btn-info btn-lg" style={{color:"white"}} onClick={this.handleClick} name="close_new_category_form">Close</button>
                                </div>
                            </div>
                        </div>   
                    :  
                    false}
                </div>
            </div>
        )
    }
    
    componentDidMount=()=>{
        window.scrollTo(0, 0);
        if(this.props.poll_name){
            this.get_groups()
            this.get_categories()
        }
    }
    componentDidUpdate(prevProps) {
        if (prevProps.poll_name !== this.props.poll_name) { 
            this.get_groups()
            this.get_categories()
        }
    }

    group_selection =()=>{
        var groups = this.state.groups.map(group=>{
            return(
                <option key={group.id} value={group.name} className="form-control">{group.name}</option>
            )
        })
        return groups
    }

    get_groups=()=>{
        fetch(`${HOST}/polls/getGroups/${this.props.poll_name}/`)
        .then(response => response.json())
        .then(response=>{
            this.setState({
                groups:response,
            })
        })
    }

    get_categories=()=>{
        fetch(`${HOST}/polls/${this.props.poll_name}/management/categories/`)
        .then(response => response.json())
        .then(response=>{
            this.setState({
                categories:response
            })
        })
    }

    display_categories=()=>{
        var categories = this.state.categories.map(category=>{
            if(this.state.query.trim()){
                //console.log(this.state.query)
                if(category.name.includes(this.state.query)){
                    return(
                        <Category
                            key = {category.id}
                            poll_name = {this.props.poll_name}
                            is_active = {this.props.is_active}
                            category = {category}
                            groups = {this.state.groups}
                            reload = {this.get_categories}
                        />
                    )
                }
            }
            else{
                return(
                    <Category
                        key = {category.id}
                        poll_name = {this.props.poll_name}
                        is_active = {this.props.is_active}
                        category = {category}
                        groups = {this.state.groups}
                        reload = {this.get_categories}
                    />
                )
            }
        })
        return categories
    }

    handleClick=(event)=>{
        if(event.target.name === "add_category_button"){
            this.setState({
                add_category: true
            })
        }
        else if(event.target.name === "close_new_category_form"){
            this.setState({
                add_category: false,
                new_category:{
                    name:"",
                    group:""
                }
            })
        }
    }  

    handleChange=(event)=>{
        if(event.target.classList.contains("form_input")){
            if(event.target.name === "category_name"){
                this.state.new_category.name = event.target.value
            }
            else if(event.target.name === "category_group"){
                this.state.new_category.group = event.target.value
            }
        }
    }  

    add_category=()=>{
        fetch(`${HOST}/polls/${this.props.poll_name}/management/categories/`,{
            method:'POST',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                'name' : this.state.new_category.name,
                'group' : this.state.new_category.group
            }),
        })
        .then(response=>{
            if(response.status != 201){
                alert("Error Occured")
            }
            document.getElementsByName('close_new_category_form')[0].click()
            this.get_categories()
        })
    }

    query_categories=()=>{
        const query = document.getElementById('query_input').value
        this.setState({
            query:query
        })
    }
}


class Category extends React.Component{
    constructor(props){
        super(props)
        this.state={            
            editing : false,
            edit_category:{
                name:"",
                group:"",
            }
        }
    }

    render(){
        if(this.state.editing){
            var group_selection = this.group_selection()
                return(
                    <div className="container-center-column container-overlay">
                        <div className="display-overlay">
                            <form>
                                <h3 className="text-center capitalize">{this.props.category.name}</h3><br/>

                                <div className="form-group">
                                    <label>Name</label>
                                    <input className="form-control form_input capitalize" name="category_name" defaultValue ={this.props.category.name} onChange={this.handleChange}></input>
                                </div>
                            
                                <div className="form-group">
                                    <label>Group</label>
                                    <select className="form-control form_input" name="category_group" onChange={this.handleChange} defaultValue={this.props.category.group_name}>
                                        <option className="form-control" >None</option>
                                        {group_selection}
                                    </select>
                                </div><br/>

                                <div className="container-center-column ">
                                    <button type="button" className="btn btn-success" onClick={this.submit_edit}>SAVE</button><br/>
                                    <button type="button" className="btn btn-danger" onClick={this.clear_candidates}>CLEAR CANDIDATES</button><br/>
                                    <button type="button" className="btn btn-danger" onClick={this.delete_category}>DELETE</button><br/>
                                </div>

                            </form>
                        </div>
                        <div className="container-center-row lone-btn">
                            <button onClick={this.close_edit} className="btn btn-info">Close</button>
                        </div>
                    </div>
                )
        }
        else{
            return(
                <div className="category-card col-md-12">
                    <h2>{this.props.category.name}</h2>
                    <h3>{this.props.category.number_candidates}
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-people-fill" viewBox="0 0 16 16">
                            <path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                            <path fillRule="evenodd" d="M5.216 14A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216z"/>
                            <path d="M4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/>
                        </svg>
                    </h3>
                    <h3>{this.props.category.group_name} Group</h3>
                    {!this.props.is_active ? 
                        <button className ="btn btn-primary" onClick={this.edit_category} >EDIT</button> 
                    :
                        false
                    }
                </div>
            )
        }
    }

    group_selection =()=>{
        var groups = this.props.groups.map(group=>{
            return(
                <option key={group.id} value={group.name} className="form-control capitalize">{group.name}</option>
            )
        })
        return groups
    }

    edit_category=()=>{
        this.setState({
            editing:true
        })
    }

    close_edit=()=>{
        this.setState({
            editing:false,
            edit_category:{
                name:"",
                group:"",
            }
        })
    }

    submit_edit=()=>{
        if(confirm('Do you want to save changes?')){
            this.close_edit()
            //console.log(this.props.category.id, this.state.edit_category.name , this.state.edit_category.group)
            fetch(`${HOST}/polls/${this.props.poll_name}/management/categories/`,{
                method:'PUT',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    "id" : this.props.category.id,
                    "action" : "edit_category",
                    'name' : this.state.edit_category.name,
                    'group_name' : this.state.edit_category.group
                }),
            })
            .then(response=>{
                if(response.status === 400){
                    alert("Error Occured")
                }
                this.props.reload()
            })
        }
    }

    clear_candidates=()=>{
        if(confirm('Do you want to clear candidates?')){
            this.close_edit()
            fetch(`${HOST}/polls/${this.props.poll_name}/management/categories/`,{
                method:'PUT',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    "id" : this.props.category.id,
                    "action" : "clear_candidates"
                }),
            })
            .then(response=>{
                if(response.status === 400){
                    alert("Error Occured")
                }
                this.props.reload()
            })
        }
    }

    delete_category=()=>{
        if(confirm('Do you want to delete?')){
            this.close_edit()
            fetch(`${HOST}/polls/${this.props.poll_name}/management/categories/`,{
                method:'DELETE',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    "id" : this.props.category.id,
                }),
            })
            .then(response=>{
                if(response.status === 400){
                    alert("Error Occured")
                }
                this.props.reload()
            })
        }
    }

    
    handleChange=(event)=>{
        if(event.target.classList.contains("form_input")){
            //console.log(event.target.value)
            if(event.target.name === "category_name"){
                this.state.edit_category.name = event.target.value
            }
            else if(event.target.name === "category_group"){
                this.state.edit_category.group = event.target.value
            }
        }
    }  
}