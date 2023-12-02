clear all
load 2Q_tomo_.mat
QSTd = data;
% QSTd = ones(3,3,4)/4; % QSTd(q1,q2,bs);   qi : 1 for X, 2 for Y, 3 for Z
QSTd_ext = zeros(4,4,4); % QSTd(q1,q2,bs);   qi : 1 for X, 2 for Y, 3 for Z, 4 for I
QSTd_ext(1:3, 1:3, :) = QSTd;

%%%% generate IX IY IZ XI YI ZI II data
QSTd_ext(4, 1:3, :) = QSTd(1, 1:3, :); 
QSTd_ext(1:3, 4, :) = QSTd(1:3, 1, :); 
QSTd_ext(4, 4, :) = QSTd(1, 1, :);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
bit_stream = [0 0; 0 1; 1 0; 1 1];
XYZ_table(:,:,1) = [0 1; 1 0]; % X
XYZ_table(:,:,2) = [0 1i; -1i 0]; % Y
XYZ_table(:,:,3) = [-1 0; 0 1]; % Z
I = [1 0;0 1]; %Identity


lo = zeros(4,4); %density matrix
for q1 = 1:4 %1 for X, 2 for Y, 3 for Z, 4 for I
    for q2 = 1:4
   
        for bs = 1:4 %bit_stream = [0 0; 0 1; 1 0; 1 1];
            %%%%%%%%%%%%% q1
            if(q1==4)% 4 for q1's I measurement
                q1_M = I;
                eig_q1_M = 1;
            else
                q1_M = XYZ_table(:,:,q1);
                eig_q1_M = (-1)^(1-bit_stream(bs, 1));
            end

            %%%%%%%%%%%%% q2
            if(q2==4)% 4 for q2's I measurement
                q2_M = I;
                eig_q2_M = 1;
            else
                q2_M = XYZ_table(:,:,q2);
                eig_q2_M = (-1)^(1-bit_stream(bs, 2));
            end

            %%%%%%%%%%%%%%%%%%%%%%
            q1q2_M = kron(q1_M,q2_M);
            eig_q1q2_M = eig_q1_M*eig_q2_M;
            lo = lo+eig_q1q2_M*QSTd_ext(q1,q2,bs)*q1q2_M;
     
        end% for bs = 1:4
             
    end%for q2 = 1:4
end%for q1 = 1:4
lo = lo/(2^2);
bar3(abs(lo))