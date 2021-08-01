class ResultsManagement extends React.Component{
    constructor(props){
        super(props)
        this.state={
            groups:[],
            grouped:"unavailable",
            view :''
        }
    }

    render(){
        let groups_btns = this.setUP_groups()
        return(
            <div>
                <div>
                    <div className="changeGroup-buttons">
                        {groups_btns}  
                    </div>
                </div>

                <div>
                    <Group 
                        key={this.state.view}
                        group_name = {this.state.view}
                        grouped ={this.state.grouped}
                    />
                </div>
            </div>
        )
    }

    componentDidMount(){
        this.get_groups()
    } 

    get_groups=()=>{
        fetch(`${HOST}/polls/getGroups/${POLL_NAME}/`)
        .then(response => response.json())
        .then(response=>{
            if(response.length > 0){
                this.setState({
                    groups:response,
                    grouped:true,
                    view:response[0].name
                })
            }else{
                this.setState({
                    grouped:false
                })
            }
        })
    }

    setUP_groups=()=>{
        if(this.state.grouped === "unavailable"){
            return false
        }
        else if (this.state.grouped){
            var all_groups_mapped = this.state.groups.map(group=>{  
                var class_add = "btn-default"
                if(group.name === this.state.view){
                    class_add = "btn-primary"
                }
                return (
                    <button key={group.id} className={`btn ${class_add} group-button`} id={group.name} onClick={()=>this.changeGroup(group.name)}>
                        {group.name}
                    </button>
                )
            })  
            return all_groups_mapped 
        }
    }

    changeGroup=(name)=>{
        window.scrollTo(0, 0);
        var all_buttons = document.querySelectorAll('.group-buttons')
        all_buttons.forEach(button=>{
            if(button.id === name){
                button.classList.remove('btn-default')
                button.classList.add('btn-primary')
            }else{
                button.classList.add('btn-default')
                button.classList.remove('btn-primary')
            }
        })
        this.setState({
            view:name
        })
    }
}

class Group extends React.Component{
    constructor(props){
        super(props)
        this.state={
            categories:[],
            view :'',
            display_direction:"column",
            pagination:{
                has_next:false,
                has_previous:false,
                num_pages:"",
                number:"",
                next_page_number:"",
                previous_page_number:""

            }, 
        }
    }

    render(){
        var display_categories = this.display_categories()
        if(this.props.grouped === "unavailable" | this.state.categories.length < 1){
            return(
                <div></div>
            )
        }
        else{
            return(
                <React.Fragment> 
                    <div className="voting-page-main">
                        <div className="categories-index">
                            {display_categories}
                        </div>

                        <div className="candidates-index">
                            <Category 
                                key={this.state.view}
                                category ={this.state.view}
                                changeCategory = {this.changeCategory}
                            />
                        </div>
                    </div>
                </React.Fragment>
            )
        }
    }

    componentDidMount=()=>{
        if(this.props.grouped === "unavailable"){
            return false
        }
        else{
            this.get_categories()
        }
        this.check_display_direction()
        window.addEventListener('resize', this.check_display_direction);
    }

    check_display_direction=()=>{
        if (window.innerWidth <= 970){
            this.setState({
                display_direction:"row"
            })
        }else{
            this.setState({
                display_direction:"column"
            })
        }
    }

    componentDidUpdate(prevProps) {
        if (this.props.grouped === "unavailable") { 
            return false
        }
        if (prevProps.grouped !== this.props.grouped) { 
            this.get_categories()
        }
    }

    get_categories=()=>{
        var group_name = this.props.group_name
        if(!this.props.grouped){
            group_name = "none"
        }
        fetch(`${HOST}/polls/getCategories/${POLL_NAME}/${group_name}/`)
        .then(response => response.json())
        .then(response=>{
            const size = response.length
            var has_next = false
            if(size > 1){
                has_next = true
            }
            this.setState({
                categories:response,
                view:response[0].name,
                pagination:{
                    has_next:has_next,
                    has_previous:false,
                    num_pages:size,
                    page_number:1,
                    next_page_number:2,
                    previous_page_number:0
    
                }
            })
        })
    }

    display_categories=()=>{
        var categories = this.state.categories.map((category,index)=>{  
            var class_add = "btn-default"
            if(category.name === this.state.view){
                class_add = "btn-info"
            }

            if(this.state.display_direction === "row"){
                if((index+1) !== this.state.pagination.page_number){
                    return
                }
                
                return (
                    <div key={category.id}>
                        <button  className={`btn ${class_add} category-button`} id={category.name} onClick={()=>this.changeCategory(category.name)}>
                            {category.name}
                        </button>
                        {/* Pagnition */}
                        <div>
                            <div className="conatiner-fluid">
                                <div className="container-center-row" >
                                    <div style={{marginRight:"1em"}}>
                                        {this.state.pagination.has_previous?
                                            <button className="btn btn-primary btn-lg" onClick={()=>{this.pag_change(-1)}}>prev</button>
                                            :
                                            <button className="btn btn-lg">prev</button>
                                        }
                                    </div>
                                    {this.state.pagination.page_number} / {this.state.pagination.num_pages}
                                    <div style={{marginLeft:"1em"}}>
                                        {this.state.pagination.has_next?
                                            <button className="btn btn-primary btn-lg" onClick={()=>{this.pag_change(1)}}>next</button>
                                            :
                                            <button className="btn btn-lg">next</button>
                                        }
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )

            }
            else{
                return (
                    <React.Fragment key={category.id}>
                        <button  className={`btn ${class_add} category-button`} id={category.name} onClick={()=>this.changeCategory(category.name)}>
                            {category.name}
                        </button>
                    </React.Fragment>
                )
            }
        })  
        return categories 
    }

    changeCategory=(name)=>{
        window.scrollTo(0, 0);
        var all_buttons = document.querySelectorAll('.category-button')

        if(!name){
            var current_index = NaN
            this.state.categories.forEach((category,index)=>{
                if(category.name === this.state.view){
                    current_index = index
                    //console.log(category.name, current_index)
                }
            })
            var goto_index = current_index + 1
            if(all_buttons.length < (goto_index + 1)){
                goto_index = 0
            }
            all_buttons.forEach((button,index)=>{
                if(index === goto_index){
                    button.classList.remove('btn-default')
                    button.classList.add('btn-info')
                    this.setState({
                        view: button.id
                    })
                }else{
                    button.classList.add('btn-default')
                    button.classList.remove('btn-info')
                }
            })  
            return false
        }

        all_buttons.forEach(button=>{
            if(button.id === name){
                button.classList.remove('btn-default')
                button.classList.add('btn-info')
            }else{
                button.classList.add('btn-default')
                button.classList.remove('btn-info')
            }
        })
        this.setState({
            view:name
        })
    } 

    pag_change=(number)=>{
        var new_page = this.state.pagination.page_number + number 
        if(new_page < 1 | new_page > this.state.pagination.num_pages){
            new_page = this.state.pagination.page_number
        }else{
            this.state.pagination.has_next = false
            this.state.pagination.has_previous = false
            if(this.state.pagination.num_pages > new_page){
                this.state.pagination.has_next = true
            }
            if(new_page > 1){
                this.state.pagination.has_previous = true
            }
        }

        this.state.pagination.page_number = new_page
        this.state.categories.forEach((category,index)=>{
            //console.log(index)
            if((index + 1) === new_page){
                this.setState({
                    view:category.name
                })
            }
        })
    }
}

class Category extends React.Component{
    constructor(props){
        super(props)
        this.state={
            results:[],
            sorted:false
        }
    }

    render(){
        var show_all_results = this.display_results()
        return(
            <div>
                <div className="lone-btn" style={{marginTop:"0px"}}>
                    <button className="btn btn-primary sort-btn" name="position_sort" onClick={()=>{this.get_results("yes")}}>SORT VOTES</button>
                    <button className="btn btn-default sort-btn" name="detail_sort" onClick={()=>{this.get_results("no")}}>DETAILED</button>
                </div>

                <table className="table table-bordered table-hover">
                    <thead className="thead-dark">
                        <tr>
                            {this.state.sorted?
                                <th scope="col">Positions</th>
                            :
                                false
                            }
                            <React.Fragment>
                                <th scope="col">Candidate</th>
                                <th scope="col">Votes</th>
                            </React.Fragment>
                        </tr>
                    </thead>
                    <tbody>
                        {show_all_results}
                    {this.state.sorted?
                            <tr>
                                <td >... </td>
                                <td >OTHERS </td>
                                <td >0</td>
                            </tr>
                        :
                            false
                    }
                    </tbody>
                </table>
            </div>
        )
    }

    componentDidMount=()=>{
        this.get_results("yes")
    }

    get_results=(sort)=>{
        var buttons = document.querySelectorAll(".sort-btn")
        buttons.forEach(button=>{
            if(sort === "yes"){
                if(button.name === "position_sort"){
                    button.classList.remove('btn-default')
                    button.classList.add('btn-primary')
                }
                else{
                    button.classList.add('btn-default')
                    button.classList.remove('btn-primary')
                }
            }
            else{
                if(button.name === "position_sort"){
                    button.classList.add('btn-default')
                    button.classList.remove('btn-primary')
                }
                else{
                    button.classList.remove('btn-default')
                    button.classList.add('btn-primary')
                }
            }
        })
        fetch(`${HOST}/polls/get_results/${POLL_NAME}/${this.props.category}/${sort}`)
        .then(response => response.json())
        .then(response=>{
            //console.log(response.candidates)
            var sorted = false
            if(sort=="yes"){
                sorted = true
            }
            this.setState({
                results:response.candidates,
                sorted:sorted
            })
        })
    }
    
    display_results=()=>{
        var count = 0
        var highest = 0
        var results = this.state.results.map((candidate)=>{
            count = count + 1
            if(candidate.votes === highest){
                count = count - 1
            }
            else{
                highest = candidate.votes
            }
            return(
                <React.Fragment key={candidate.id}>
                    <tr>
                        {this.state.sorted?
                            <td >{count} </td>
                        :
                            false
                        }
                        <td>
                            <img style={{height:"90px",width:"90px"}} className="rounded-circle" src={candidate.image}/> 
                            <br></br>
                            <p>
                                <strong>
                                    {candidate.name} 
                                </strong>
                            </p><br></br>
                            <p>
                                {candidate.party}
                            </p>
                        </td>
                        <td >{candidate.votes} </td>
                    </tr>
                </React.Fragment>
            )
        })
        return results
    }
}

ReactDOM.render(<ResultsManagement/>,document.querySelector('#body'));
//console.log(POLL_NAME)

