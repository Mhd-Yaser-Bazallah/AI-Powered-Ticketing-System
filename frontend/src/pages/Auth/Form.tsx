import { useFormik } from 'formik';
import { useLogin } from '../../Hooks/useAuth';
import Loading from '../../components/Button/Loading';
import { Input } from '../../components/Input/Text';
import { LoginInitialValues, LoginSchema } from '../../validation/Auth';

const LoginForm = () => {
    const mutation: any = useLogin();
    const handleSubmit = async (values: any, { resetForm }: any) => {
        mutation.mutate(values, {
            onSuccess: async (res: any) => {

            },
        });
    };
    const formik = useFormik({
        initialValues: LoginInitialValues,
        validationSchema: LoginSchema,
        onSubmit: handleSubmit,
    });
    return (
        <div className="">
            <form className="space-y-5 w-full dark:text-white" onSubmit={formik.handleSubmit}>
                <Input
                    names={["email"]}
                    labels={["Email Address"]}
                    formik={formik}
                    type='email'
                />
                <Input
                    names={["password"]}
                    labels={["password"]}
                    formik={formik}
                    type='password'
                />
                <Loading mutation={mutation.isLoading} title={"Sgin in"} />
            </form>
        </div>
    );
};

export default LoginForm;
