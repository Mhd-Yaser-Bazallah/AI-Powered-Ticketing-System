import React, { useState } from 'react';
import { useFormik } from 'formik';
import { Signup } from '../../Hooks/useSignup';
import Loading from '../../components/Button/Loading';
import { Input } from '../../components/Input/Text';
import { SignupSchema } from '../../validation/Signup';
import { AuthInstance } from '../../services/APIs/Auth';

const MIN_COMPANY_LENGTH = 1;
let debounceTimer: NodeJS.Timeout;

const SignUpForm = ({ setIsFlipped }: any) => {
  const mutation = Signup();
  const [companyCheck, setCompanyCheck] = useState<'valid' | 'invalid' | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [companyId, setCompanyId] = useState<string | null>(sessionStorage.getItem('company_id'));

  const handleSubmit = async (values: any, { resetForm }: any) => {
    const payload = {
      ...values,
      company_id: companyId,
    };

    mutation.mutate(payload, {
      onSuccess: async (res) => {
        if (res?.status === 201) {
          resetForm();
          sessionStorage.removeItem('company_id');
          setIsFlipped(false);
        }
      },
    });
  };

  const handleCompanyChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = event.target;
    setCompanyCheck(null);
    setIsChecking(false);
    clearTimeout(debounceTimer);

    if (value.trim().length >= MIN_COMPANY_LENGTH) {
      setIsChecking(true);
      debounceTimer = setTimeout(async () => {
        try {
          const response = await AuthInstance.MakeCheckForEmail({ email: value });
          if (response.status === 200 && response.data?.id) {
            setCompanyCheck('valid');
            setCompanyId(response.data.id); 
            sessionStorage.setItem('company_id', response.data.id);
          } else {
            setCompanyCheck('invalid');
            setCompanyId(null);
          }
        } catch (error) {
          setCompanyCheck('invalid');
          setCompanyId(null);
        } finally {
          setIsChecking(false);
        }
      }, 500);
    }
  };

  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
      username: '',
      phone_number: '',
      company: '', 
    },
    validationSchema: SignupSchema,
    onSubmit: handleSubmit,
  });

  return (
    <div>
      <form className="space-y-5 w-full dark:text-white" onSubmit={formik.handleSubmit}>
        <Input
          names={['email']}
          labels={['Email Address']}
          formik={formik}
          type="email"
        />
        <Input
          names={['password']}
          labels={['Password']}
          formik={formik}
          type="password"
        />
        <Input
          names={['username']}
          labels={['Username']}
          formik={formik}
          type="text"
        />
        <div className="relative">
          <Input
            names={['company']}
            labels={['Company']}
            formik={formik}
            type="text"
            onChange={handleCompanyChange}
          />
          <div className="absolute top-[58px] right-3 transform -translate-y-1/2">
            {isChecking && (
              <div className="animate-spin w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full"></div>
            )}
            {!isChecking && companyCheck === 'valid' && (
              <span className="text-green-600">✔️</span>
            )}
            {!isChecking && companyCheck === 'invalid' && (
              <span className="text-red-600">❌</span>
            )}
          </div>
        </div>
        <Input
          names={['phone_number']}
          labels={['Phone Number']}
          formik={formik}
          type="number"
        />
        <Loading mutation={mutation.isLoading} title="Sign up" />
      </form>
    </div>
  );
};

export default SignUpForm;
