import { useFormik } from "formik";
import toast from "react-hot-toast";
import { Delete as Delete_request, Edit, Get } from "../../Hooks/useProfile";
import { Input } from "../../components/Input/Text";
import Delete from "../../components/Modal/Delete";
import { default as TableSkeleton } from '../../components/Skeleton/Table';
const Index = () => {
  const Profile: any = Get(sessionStorage.getItem('id'));
  const mutation: any = Edit();

  const formik:any = useFormik({
    initialValues: {
      phone_number: Profile?.data?.data?.phone_number || "",
      company: Profile?.data?.data?.company || "",
      email: Profile?.data?.data?.email || "",
      username: Profile?.data?.data?.username || "",
    },
    enableReinitialize: true,
    onSubmit: async (values) => {
      handleChangeProfile(values);
    },
  });

  const handleChangeProfile = async (values: any) => {
    // Get only changed values
    const changedValues = Object.keys(values).reduce((acc: any, key) => {
      if (values[key] !== formik.initialValues[key]) {
        acc[key] = values[key];
      }
      return acc;
    }, {});
  
    if (Object.keys(changedValues).length === 0) {
      toast("No changes made!", { icon: "ℹ️" });
      return;
    }
  
    toast.promise(
      mutation.mutateAsync(changedValues),
      {
        loading: "Saving...",
        success: "Profile Updated!",
        error: "Could not update!",
      }
    );
  };


  return (
    <>

      {Profile.isLoading && (
        <TableSkeleton />
      )}
      {!Profile.isLoading && (
        <div>
          <form
            onSubmit={formik.handleSubmit}
            className="border border-[#ebedf2] shadow-lg dark:border-[#191e3a] rounded-md p-4 mb-5 bg-white dark:bg-black"
          >
            <div className="flex justify-between">
              <h6 className="text-lg font-bold mb-5">Profile Information</h6>
              <Delete id={sessionStorage.getItem('id')} query_name={Delete_request} label_of_button="Delete" title="delete My Profile!" />

            </div>
            <div className="flex flex-col sm:flex-row">
              <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-5">
                <Input
                  names={["username"]}
                  labels={["User Name"]}
                  formik={formik}
                  type="text"
                />
                <Input
                  names={["email"]}
                  labels={["Email"]}
                  formik={formik}
                  type="email"
                />
                <Input
                  names={["company"]}
                  labels={["Company"]}
                  formik={formik}
                  type="text"
                />
                <Input
                  names={["phone_number"]}
                  labels={["Phone Number"]}
                  formik={formik}
                  type="number"
                />

              </div>
            </div>
            <button
              type="submit"
              className="btn btn-outline-secondary text-black mx-auto w-full px-4 py-2 rounded-md"
              disabled={mutation.isLoading}
            >
              {mutation.isLoading ? "Saving..." : "Edit My Profile"}
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default Index;
