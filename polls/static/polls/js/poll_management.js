class PollManagement extends React.Component{
    constructor(props){
        super(props)
        this.state={            
            view : PAGE_VIEW,
            poll_settings:"",
            poll_name : POLL_NAME
        }
    }

    render(){
       
        return(
            <div>
                {/* Change page view to categories or candidates or settings */}
                <div className="changeView-buttons">
                    <button className="btn btn-lg change_view_btns" name="categories" onClick={this.change_view}>
                        Categories
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-tags-fill" viewBox="0 0 16 16">
                            <path d="M2 2a1 1 0 0 1 1-1h4.586a1 1 0 0 1 .707.293l7 7a1 1 0 0 1 0 1.414l-4.586 4.586a1 1 0 0 1-1.414 0l-7-7A1 1 0 0 1 2 6.586V2zm3.5 4a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/>
                            <path d="M1.293 7.793A1 1 0 0 1 1 7.086V2a1 1 0 0 0-1 1v4.586a1 1 0 0 0 .293.707l7 7a1 1 0 0 0 1.414 0l.043-.043-7.457-7.457z"/>
                        </svg>
                    </button>
                    <button className="btn btn-lg change_view_btns" name="candidates" onClick={this.change_view}>
                        Candidates
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-people-fill" viewBox="0 0 16 16">
                            <path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                            <path fillRule="evenodd" d="M5.216 14A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216z"/>
                            <path d="M4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/>
                        </svg>
                    </button>
                    <button className="btn btn-lg change_view_btns" name="settings" onClick={this.change_view}>
                        Settings
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-gear" viewBox="0 0 16 16">
                            <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/>
                            <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/>
                        </svg>
                    </button>
                </div> 

                <div>
                    {this.state.view === "categories"?
                            <CategoriesMgt
                                poll_name = {this.state.poll_settings.name}
                                is_active = {this.state.poll_settings.is_active}
                            />   
                        : 
                            false               
                    }   
                    {this.state.view === "candidates"?
                            <CandidatesMgt
                                poll_name = {this.state.poll_settings.name}
                                is_active = {this.state.poll_settings.is_active}
                            /> 

                        : 
                            false               
                    }   
                    {this.state.view === "settings"?
                            <Settings
                                settings = {this.state.poll_settings}
                                get_settings = {this.get_settings}
                            />   
                        : 
                            false               
                    }                     
                </div>          
                
            </div>     
        )
    }

    componentDidMount=()=>{
        var page_view = this.state.view
        if(!page_view){
            page_view = "categories"
            this.setState({
                view : "candidate"
            })
        }
        document.querySelectorAll('.change_view_btns').forEach(button=>{
            if(button.name === page_view){
                button.classList.add("btn-info")
            }
        })
        this.get_settings()
    }

    change_view=(event)=>{
        document.querySelectorAll('.change_view_btns').forEach(button=>{
            button.classList.remove("btn-info")
        })
        this.setState({
            view : event.target.name
        })
        event.target.classList.add("btn-info")
        const BASE_URL = `${HOST}/polls/manage/${this.state.poll_name}`
        window.history.pushState("x","xx",`${BASE_URL}/${event.target.name}/`)
    }

    get_settings=(new_name)=>{
        var poll_name = this.state.poll_name
        if(new_name){
            poll_name = new_name
        }
        fetch(`${HOST}/polls/${poll_name}/management/settings/`)
        .then(response => response.json())
        .then(response=>{
            this.setState({
                poll_settings:response,
                poll_name:response.name
            })
            // console.log(response)
        })
    }
}

ReactDOM.render(<PollManagement />,document.querySelector('#body'));
// console.log(PAGE_VIEW,POLL_NAME)