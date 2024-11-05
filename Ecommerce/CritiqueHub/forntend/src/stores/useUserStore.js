import {create} from "zustand";
import axios from "../lib/axios";
import {toast} from"react-hot-toast";

 export const useUserStore = create((set) => ({
    user:null,
    loading:false,
    checkingAuth:true,

    signup:async({name,email,password,confirmPassword})=>{
        set({loading:true});
        if(password !== confirmPassword){
            set({loading:false});
            return toast.error("Passwords do not match");
        }
        try{
            const res=await axios.post("/auth/signup",{name,email,password});
            set({ user:res.data.user,loading:false});
        }catch(error){
            set({loading:false});
            toast.error(error.response.data.message||"Something went wrong");
        }
    },
}));