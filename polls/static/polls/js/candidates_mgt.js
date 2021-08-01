class CandidatesMgt extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            candidates : [], 
            categories : [],
            add_candidate:false,
            error_message:"",
            new_candidate:{
                name:"",
                party:"",
                categories:[]
            },
            query:""
        }  
    }

    render(){
        var candidates = this.display_candidates()
        var categories_selection = this.categories_selection()
        return(
            <div className="container-fluid">
                <div className="container-center-row lone-btn" >
                    {this.props.is_active ?
                        false
                    :
                        <button className="btn btn-outline-primary btn-lg" name="add_candidate_button" onClick={this.handleClick} >
                            Add Candidate 
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-plus-circle-dotted" viewBox="0 0 16 16">
                                <path d="M8 0c-.176 0-.35.006-.523.017l.064.998a7.117 7.117 0 0 1 .918 0l.064-.998A8.113 8.113 0 0 0 8 0zM6.44.152c-.346.069-.684.16-1.012.27l.321.948c.287-.098.582-.177.884-.237L6.44.153zm4.132.271a7.946 7.946 0 0 0-1.011-.27l-.194.98c.302.06.597.14.884.237l.321-.947zm1.873.925a8 8 0 0 0-.906-.524l-.443.896c.275.136.54.29.793.459l.556-.831zM4.46.824c-.314.155-.616.33-.905.524l.556.83a7.07 7.07 0 0 1 .793-.458L4.46.824zM2.725 1.985c-.262.23-.51.478-.74.74l.752.66c.202-.23.418-.446.648-.648l-.66-.752zm11.29.74a8.058 8.058 0 0 0-.74-.74l-.66.752c.23.202.447.418.648.648l.752-.66zm1.161 1.735a7.98 7.98 0 0 0-.524-.905l-.83.556c.169.253.322.518.458.793l.896-.443zM1.348 3.555c-.194.289-.37.591-.524.906l.896.443c.136-.275.29-.54.459-.793l-.831-.556zM.423 5.428a7.945 7.945 0 0 0-.27 1.011l.98.194c.06-.302.14-.597.237-.884l-.947-.321zM15.848 6.44a7.943 7.943 0 0 0-.27-1.012l-.948.321c.098.287.177.582.237.884l.98-.194zM.017 7.477a8.113 8.113 0 0 0 0 1.046l.998-.064a7.117 7.117 0 0 1 0-.918l-.998-.064zM16 8a8.1 8.1 0 0 0-.017-.523l-.998.064a7.11 7.11 0 0 1 0 .918l.998.064A8.1 8.1 0 0 0 16 8zM.152 9.56c.069.346.16.684.27 1.012l.948-.321a6.944 6.944 0 0 1-.237-.884l-.98.194zm15.425 1.012c.112-.328.202-.666.27-1.011l-.98-.194c-.06.302-.14.597-.237.884l.947.321zM.824 11.54a8 8 0 0 0 .524.905l.83-.556a6.999 6.999 0 0 1-.458-.793l-.896.443zm13.828.905c.194-.289.37-.591.524-.906l-.896-.443c-.136.275-.29.54-.459.793l.831.556zm-12.667.83c.23.262.478.51.74.74l.66-.752a7.047 7.047 0 0 1-.648-.648l-.752.66zm11.29.74c.262-.23.51-.478.74-.74l-.752-.66c-.201.23-.418.447-.648.648l.66.752zm-1.735 1.161c.314-.155.616-.33.905-.524l-.556-.83a7.07 7.07 0 0 1-.793.458l.443.896zm-7.985-.524c.289.194.591.37.906.524l.443-.896a6.998 6.998 0 0 1-.793-.459l-.556.831zm1.873.925c.328.112.666.202 1.011.27l.194-.98a6.953 6.953 0 0 1-.884-.237l-.321.947zm4.132.271a7.944 7.944 0 0 0 1.012-.27l-.321-.948a6.954 6.954 0 0 1-.884.237l.194.98zm-2.083.135a8.1 8.1 0 0 0 1.046 0l-.064-.998a7.11 7.11 0 0 1-.918 0l-.064.998zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
                            </svg>
                        </button>
                    }
                </div><br/>
                <div className="container-center-row">
                    <div className="search-box" style={{width:"70%"}}>    
                        <input className="form-control" id="query_input" type="text" placeholder="filter"></input>
                        <button type="submit" name="search_button" onClick={this.query_candidates}><i className="form-control fa fa-search"></i></button>   
                    </div>
                </div>

                <div className="container-fluid">
                    <div className="candidates-index">
                        <div className="candidates-container-mgt row" >
                            {candidates}
                        </div>
                    </div>
                </div>

                <div>
                    {this.state.add_candidate ?
                        <div className = "container-center-column container-overlay">
                            <div className="display-overlay">
                                <form>
                                    <div className="form-group">
                                        <label>Name</label>
                                        <input className="form-control capitalize" type="text" name="candidate_name" size='80' onChange={this.handleChange}></input>
                                    </div>
                                    <div className="form-group">
                                        <label>Party</label>
                                        <input className="form-control" type="text" name="candidate_party" size='80' onChange={this.handleChange}></input>
                                    </div>
                                    <div className="form-group">
                                        <label>Image</label>
                                        <input className="form-control-file" id="new_candidate_image" name="image" type="file" ></input>              
                                    </div>
                                    <div>
                                        <h2 style={{textDecoration:"underline", marginTop:"2em", marginBottom:"2em"}}>Categories contesting</h2>
                                        {categories_selection}
                                    </div>
                                    <div className="container-center-row lone-btn">
                                        <button type="button" className="btn btn-lg btn-success" style={{color:"white"}} onClick={this.add_candidate}>Add</button>
                                    </div>
                                </form>
                            </div>
                            <div className="container-center-row lone-btn">
                                <button className="btn btn-info btn-lg" style={{color:"white"}} onClick={this.handleClick} name="close_new_candidate_form">Close</button>
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
            this.get_candidates()
            this.get_categories()
        }
    }
    componentDidUpdate=(prevProps)=> {
        if (prevProps.poll_name !== this.props.poll_name) { 
            this.get_candidates()
            this.get_categories()
        }
    }
   
    get_candidates=()=>{
        fetch(`${HOST}/polls/${this.props.poll_name}/management/candidates/`)
        .then(response => response.json())
        .then(response=>{
            this.setState({
                candidates:response
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

    display_candidates=()=>{
        var candidates = this.state.candidates.map(candidate=>{
            if(this.state.query.trim()){
                // console.log(this.state.query)
                if(candidate.name.includes(this.state.query)){
                    return(
                        <Candidate
                            key = {candidate.id}
                            poll_name = {this.props.poll_name}
                            is_active = {this.props.is_active}
                            candidate = {candidate}
                            categories = {this.state.categories}
                            get_candidates = {this.get_candidates}
                        />
                    )
                }
            }
            else{
                return(
                    <Candidate
                        key = {candidate.id}
                        poll_name = {this.props.poll_name}
                        is_active = {this.props.is_active}
                        candidate = {candidate}
                        categories = {this.state.categories}
                        get_candidates = {this.get_candidates}
                    />
                )
            }
        })
        return candidates
    }

    categories_selection=()=>{
        var categories = this.state.categories.map(category=>{
            return(
                <div key={category.id} className="form-group">
                    <label className="capitalize">{category.name}</label>
                    <input type="checkbox" value={category.name} className="categories_checkbox capitalize" name ={category.name} onChange={this.handleChange}></input>
                </div>
            )
        })
        return categories
    }

    handleClick=(event)=>{
        if(event.target.name === "add_candidate_button"){
            this.setState({
                add_candidate: true
            })
        }
        else if(event.target.name === "close_new_candidate_form"){
            this.setState({
                add_candidate: false,
                new_candidate:{
                    name:"",
                    categories:[]
                }
            })
        }
    }  

    handleChange=(event)=>{
        if(event.target.name === "candidate_name"){
            this.state.new_candidate.name = event.target.value
        }
        else if(event.target.name === "candidate_party"){
            this.state.new_candidate.party = event.target.value
        }
        else if(event.target.className.includes("categories_checkbox")){
            // console.log(event.target.checked)
            if(event.target.checked){
                this.state.new_candidate.categories.push(event.target.value)
            }
            else{
                var index = this.state.new_candidate.categories.indexOf(event.target.value)
                if(index > -1){
                    this.state.new_candidate.categories.splice(index, 1)
                }
            }
        }
        // console.log(this.state.new_candidate.categories)
    }  

    add_candidate=()=>{
        if(confirm("Add candidate ?")){
            var image = document.getElementById("new_candidate_image")
            const form_data = new FormData()

            if(image.files[0]){
                form_data.append("image",image.files[0])
            }else{
                console.log("no image chosen")
            }
            form_data.append("form_type","new_candidate")
            form_data.append("name",this.state.new_candidate.name)
            form_data.append("party",this.state.new_candidate.party)
            form_data.append("categories",this.state.new_candidate.categories)

            fetch(`${HOST}/polls/${this.props.poll_name}/management/candidates/`,{
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
                this.setState({
                    add_candidate: false,
                    new_candidate:{
                        name:"",
                        party:"",
                        categories:[]
                    }
                })
                if(response.status === 400){
                    alert("Error Occured; check length of name")
                }
                this.get_candidates()
            })
        }
    }

    query_candidates=()=>{
        const query = document.getElementById('query_input').value
        this.setState({
            query:query.toLowerCase()
        })
        console.log(query.toLowerCase())
    }
}


class Candidate extends React.Component{
    constructor(props){
        super(props)
        this.state={            
            editing : false,
            edit_candidate:{
                name:'',
                party:'',
                categories:[],
            }
        }
    }

    render(){
        if(this.state.editing){
            var categories_selection = this.categories_selection()
            return(
                <div className="container-center-column container-overlay">
                    <div className="display-overlay edit_candidate_form">
                            <div className="image"> 
                                {this.props.candidate.image ?
                                    <img className="rounded-circle" src={this.props.candidate.image} alt={this.props.candidate.name}></img>
                                :
                                    false
                                }
                            </div>
                        <form>
                            <div className="form-group">
                                <label>Name</label>
                                <input className="form-control capitalize" type="text" name="candidate_name" size='80' defaultValue={this.props.candidate.name} onChange={this.handleChange}></input>
                            </div>
                            <div className="form-group">
                                <label>Party</label>
                                <input className="form-control" type="text" name="candidate_party" size='80' defaultValue={this.props.candidate.party} onChange={this.handleChange}></input>
                            </div>
                            <div className="form-group">
                                <label>Change Image</label>
                                <input id="edit_candidate_image" className="form-control-file" name="edit_image" type="file" ></input>              
                            </div>

                            <div>
                                <h2 style={{textDecoration:"underline", marginTop:"2em", marginBottom:"2em"}}>Categories Contesting</h2>
                                {categories_selection}
                            </div>

                            <div className="container-center-row lone-btn">
                                <button type="button" className="btn btn-lg btn-success" style={{color:"white"}} onClick={this.submit_changes} >SAVE</button>
                            </div>
                        </form>
                        <div className="container-center-row lone-btn">
                            <button className="btn btn-danger btn-lg" style={{color:"white"}} onClick={this.delete_candidate}>DELETE</button>
                        </div>
                    </div>
                    <div className="container-center-row lone-btn">
                        <button className="btn btn-info btn-lg" style={{color:"white"}} onClick={this.close_edit} >CLOSE</button>
                    </div>
                </div>
            )
        }
        else{
            return(
                <div className="candidate-card col-md-6">
                    <div className="card">
                        <div className="card-image">
                            {this.props.candidate.image ?
                                <img src={this.props.candidate.image} alt={this.props.candidate.name}></img>
                            :
                                false
                            }
                        </div>
                        <h2 className="capitalize">{this.props.candidate.name}</h2>
                        <h3>{this.props.candidate.party}</h3>
                        <div>
                        {!this.props.is_active ? 
                            <button className ="btn btn-primary" onClick={this.edit_candidate}>EDIT</button> 
                        :
                            false}
                        </div>
                    </div>
                </div>
            )
        }
    }

    edit_candidate=()=>{
        this.setState({
            editing:true,
        });
        this.state.edit_candidate.name = this.props.candidate.name
        this.state.edit_candidate.party = this.props.candidate.party
        this.props.candidate.categories_contesting.forEach(category => {
            this.state.edit_candidate.categories.push(category)   
        });
    }

    close_edit=()=>{
        this.setState({
            editing: false,
            edit_candidate:{
                name:'',
                party:'',
                categories:[],
            }
        })
    }

    categories_selection=()=>{
        var categories = this.props.categories.map(category=>{
            return(
                <div key={category.id} className="form-group">
                    <label className="capitalize">{category.name}</label>
                    {this.props.candidate.categories_contesting.includes(category.name) ? 
                    <input className="categories_checkbox " type="checkbox" value={category.name} name ={category.name}  onChange={this.handleChange} defaultChecked={true}></input>
                   :
                    <input className="categories_checkbox " type="checkbox" value={category.name} name ={category.name}  onChange={this.handleChange} defaultChecked={false}></input>
                    }
                </div>
            )
        })
        return categories
    }

    handleChange=(event)=>{
        if(event.target.name === "candidate_name"){
            this.state.edit_candidate.name = event.target.value
        }
        else if(event.target.name === "candidate_party"){
            this.state.edit_candidate.party = event.target.value
            // console.log(event.target.value)
        }
        else if(event.target.className.includes("categories_checkbox")){
            if(event.target.checked){
                this.state.edit_candidate.categories.push(event.target.value)
            }
            else{
                var index = this.state.edit_candidate.categories.indexOf(event.target.value)
                if(index > -1){
                    this.state.edit_candidate.categories.splice(index, 1)
                }
            }
        }
        // console.log(this.state.edit_candidate.categories)
    } 
    
    submit_changes=()=>{
        // console.log(this.props.poll_name)
        if(confirm("Submit Changes ?")){
            var image = document.getElementById("edit_candidate_image")
            const form_data = new FormData()

            if(image.files[0]){
                form_data.append("image",image.files[0])
            }
            // else{
            //     console.log("no image chosen")
            // }
            form_data.append("form_type","edit_candidate")
            form_data.append("candidate_id",this.props.candidate.id)
            form_data.append("name",this.state.edit_candidate.name)
            form_data.append("party",this.state.edit_candidate.party)
            form_data.append("categories",this.state.edit_candidate.categories)

            fetch(`${HOST}/polls/${this.props.poll_name}/management/candidates/`,{
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
                this.setState({
                    edit_candidate:{
                        name:"",
                        categories:[]
                    }
                })
                if(response.status === 400){
                    alert("Error Occured")
                }
                this.close_edit()
                this.props.get_candidates()
            })
        }
    }

    delete_candidate=()=>{
        if(confirm('Do you want to delete?')){
            this.close_edit()
            fetch(`${HOST}/polls/${this.props.poll_name}/management/candidates/`,{
                method:'DELETE',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    "id" : this.props.candidate.id
                }),
            })
            .then(response=>{
                this.setState({
                    edit_candidate:{
                        name:"",
                        categories:[]
                    }
                })
                if(response.status === 400){
                    alert("Error Occured")
                }
                this.close_edit()
                this.props.get_candidates()
            })
        }
    }
}
