
import { useEffect, useState } from 'react';
import Dropdown from '../Dropdown';
import IconBellBing from '../Icon/IconBellBing';
import IconInfoCircle from '../Icon/IconInfoCircle';
import toast from 'react-hot-toast';
import { APIInstance } from '../../services/APIs/Notifications';

export const Notification = () => {
  const [allNotifications, setAllNotifications] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchNotifications = async () => {
    try {
      const user_id = sessionStorage.getItem('id');
      if (!user_id) {
        console.error('No user ID found in sessionStorage');
        return;
      }

      setLoading(true);
      const response = await APIInstance.Get(user_id);

      setAllNotifications(Array.isArray(response) ? response : response.data || []);
    } catch (error) {
      console.error('Error fetching notifications:', error);
      toast.error('Failed to fetch notifications');
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (id: number) => {
    const user_id = sessionStorage.getItem('id');
    if (!user_id) {
      toast.error('User ID not found!');
      return;
    }

    try {
      const res = await APIInstance.MakeRead(id, { user: user_id });
      if (res?.status === 200 || res?.success) {
        setAllNotifications((prev) =>
          prev.map((notif) =>
            notif.id === id ? { ...notif, is_read: true } : notif
          )
        );
        toast.success('Marked as read');
      }
    } catch (err) {
      console.error(err);
      toast.error('Failed to mark as read');
    }
  };

  const handleMarkAllRead = async () => {
    const user_id = sessionStorage.getItem('id');
    if (!user_id) {
      toast.error('User ID not found!');
      return;
    }

    try {
      const res = await APIInstance.MakeAllRead({ user: user_id });
      if (res?.status === 200 || res?.success) {
        setAllNotifications((prev) =>
          prev.map((notif) => ({ ...notif, is_read: true }))
        );
        toast.success('All notifications marked as read');
      }
    } catch (err) {
      console.error(err);
      toast.error('Failed to mark all as read');
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const unreadCount = allNotifications.filter((n) => !n.is_read).length;

  return (
    <div className="dropdown shrink-0">
      <Dropdown
        offset={[0, 8]}
        placement="bottom-end"
        btnClassName="relative group block"
        button={
          <div className="relative w-8 h-8 rounded-full flex justify-center items-center bg-gray-200 hover:bg-gray-300 transition">
            <IconBellBing className="w-4 h-4 text-gray-700" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1">
                {unreadCount}
              </span>
            )}
          </div>
        }
      >
        <ul className="!py-0 h-[300px] overflow-auto text-dark dark:text-white-dark w-[350px] sm:w-[400px] divide-y dark:divide-white/10">
          <li onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center px-4 py-2 justify-between font-semibold sticky top-0 bg-white dark:bg-gray-900 z-10">
              <h4 className="text-lg">Notifications</h4>
              {allNotifications.length > 0 && (
                <button
                  type="button"
                  onClick={handleMarkAllRead}
                  className="text-sm text-blue-600 hover:underline"
                >
                  Mark all as read
                </button>
              )}
            </div>
          </li>

          {loading ? (
            <li className="text-center py-8 text-gray-500">Loading...</li>
          ) : allNotifications.length > 0 ? (
            allNotifications.map((notif) => (
              <li
                key={notif.id}
                className={`px-4 py-3 border-b hover:bg-gray-50 transition ${
                  !notif.is_read ? 'bg-gray-50' : ''
                }`}
              >
                <div className="flex justify-between items-start">
                  <p className="text-sm text-gray-800 dark:text-gray-200 leading-5">
                    {notif.message}
                  </p>
                  {!notif.is_read && (
                    <button
                      type="button"
                      onClick={() => handleToggle(notif.id)}
                      className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded hover:bg-green-200"
                    >
                      Mark read
                    </button>
                  )}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {new Date(notif.created_at).toLocaleString()}
                </div>
              </li>
            ))
          ) : (
            <li>
              <div className="!grid place-content-center text-center text-lg min-h-[200px]">
                <div className="mx-auto ring-4 ring-[#D69235]/30 rounded-full mb-4 text-[#D69235]">
                  <IconInfoCircle fill={true} className="w-10 h-10" />
                </div>
                No notifications yet.
              </div>
            </li>
          )}
        </ul>
      </Dropdown>
    </div>
  );
};
