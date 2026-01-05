import React, { useState } from 'react';
import { useFormik, FieldArray, FormikProvider } from 'formik';
import * as Yup from 'yup';
import Status from '../../../components/Modal/Status';
import toast from 'react-hot-toast';
import { Input } from '../../../components/Input/Text';
import { APIInstance } from '../../../services/APIs/Company';

interface CustomizeProps {
  item: any;
}

const Customize: React.FC<CustomizeProps> = ({ item }) => {
  const [modal, setModal] = useState(false);

  const formik = useFormik({
    initialValues: {
      name: '',
      company: item?.id,
      created_by: sessionStorage.getItem('id'),
      steps: [{ name: '', order: 0 }],
    },
    validationSchema: Yup.object().shape({
      name: Yup.string().required('Name is required'),
      steps: Yup.array(),
    }),
    onSubmit: async (values) => {
      toast.promise(APIInstance.AddWorkflow(values), {
        loading: 'Submitting...',
        success: 'Workflow created successfully!',
        error: 'Submission failed',
      });
      setModal(false);
    },
  });

  return (
    <>
      <button
        onClick={() => setModal(true)}
        className="bg-purple-500 text-white px-3 py-1 rounded hover:bg-purple-600"
      >
        Customize
      </button>

      <Status modal={modal} setModal={setModal}>
        <form onSubmit={formik.handleSubmit} className="space-y-4">
          <Input
            names={["name"]}
            labels={["Workflow Name"]}
            formik={formik}
            type="text"
          />

          <FormikProvider value={formik}>
            <FieldArray
              name="steps"
              render={(arrayHelpers) => (
                <div className="space-y-3">
                  {formik.values.steps.map((step, index) => (
                    <div
                      key={index}
                      className="grid grid-cols-2 gap-4 items-center border p-3 rounded bg-gray-50 dark:bg-[#1e293b]"
                    >
                      <div>
                        <input
                          type="text"
                          name={`steps[${index}].name`}
                          placeholder="Step Name"
                          onChange={formik.handleChange}
                          value={step.name}
                          className="w-full p-2 border rounded"
                        />
                        {formik.errors.steps?.[index]?.name && (
                          <div className="text-red-500 text-sm">{formik.errors.steps[index].name}</div>
                        )}
                      </div>

                      <div>
                        <input
                          type="number"
                          name={`steps[${index}].step`}
                          placeholder="Step Number"
                          onChange={formik.handleChange}
                          value={step.order}
                          className="w-full p-2 border rounded"
                        />
                        {formik.errors.steps?.[index]?.order && (
                          <div className="text-red-500 text-sm">{formik.errors.steps[index].order}</div>
                        )}
                      </div>

                      <div className="col-span-2 flex justify-end space-x-2">
                        {index > 0 && (
                          <button
                            type="button"
                            onClick={() => arrayHelpers.remove(index)}
                            className="text-sm bg-red-500 text-white px-2 py-1 rounded"
                          >
                            Remove
                          </button>
                        )}
                        {index === formik.values.steps.length - 1 && (
                          <button
                            type="button"
                            onClick={() => arrayHelpers.push({ name: '', order: index + 1 })}
                            className="text-sm bg-blue-500 text-white px-2 py-1 rounded"
                          >
                            Add Step
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            />
          </FormikProvider>

          <div className="flex justify-end pt-4">
            <button
              type="submit"
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              Confirm
            </button>
          </div>
        </form>
      </Status>
    </>
  );
};

export default Customize;
